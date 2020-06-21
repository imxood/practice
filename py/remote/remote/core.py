import os
import sys
import threading
import collections
import inspect
import textwrap
import getpass
import socket
import zlib
import codecs
import base64

from selectors import BaseSelector, DefaultSelector, EVENT_READ
from subprocess import Popen, PIPE

_v = True
_vv = True

# 128k
CHUNK_SIZE = 131072


ALLOCATE_ID = 105


def _signals(obj, signal):
    return (
        obj.__dict__
        .setdefault('_signals', {})
        .setdefault(signal, [])
    )


def listen(obj, name, func):
    """
    Arrange for `func()` to be invoked when signal `name` is fired on `obj`.
    """
    _signals(obj, name).append(func)


def unlisten(obj, name, func):
    """
    Remove `func()` from the list of functions invoked when signal `name` is
    fired by `obj`.

    :raises ValueError:
        `func()` was not on the list.
    """
    _signals(obj, name).remove(func)


def fire(obj, name, *args, **kwargs):
    """
    Arrange for `func(*args, **kwargs)` to be invoked for every function
    registered for signal `name` on `obj`.
    """
    for func in _signals(obj, name):
        func(*args, **kwargs)


class Side(object):

    def __init__(self, stream, fp, keep_alive=True):
        self.closed = False
        self.stream = stream
        # File object
        self.fp = fp
        #: File descriptor
        self.fd = fp.fileno()
        self.keep_alive = keep_alive

    def __repr__(self):
        return '<Side of %s fd %s>' % (
            self.stream.name or repr(self.stream),
            self.fd
        )

    def close(self):
        if not self.closed:
            self.closed = True
            self.fp.close()


class Stream:

    protocol = None

    def __init__(self):
        self.rfd = None
        self.wfd = None
        self.closed = True

    def set_protocol(self, protocol):

        if self.protocol:
            self.protocol.stream = None

        self.protocol = protocol
        self.protocol.stream = self

    def accept(self, rfd, wfd):
        self.rfd = rfd
        self.wfd = wfd
        self.closed = False

    def read(self, n=CHUNK_SIZE):
        if self.closed:
            return b('')
        s = os.read(self.rfd, n)
        return s

    def write(self, s):
        if self.closed:
            return 0
        written = os.write(self.wfd, s)
        return written

    def close(self):
        if self.closed:
            return
        os.close(self.rfd)
        os.close(self.wfd)
        self.closed = True

    def on_receive(self):
        buf = self.read(self.protocol.read_size)
        if not buf:
            LOG.debug('%r: empty read, disconnecting', self.receive_side)
            self.on_disconnect()
        self.protocol.on_receive(buf)

    def on_transmit(self):
        self.protocol.on_transmit()

    def on_shutdown(self):
        self.protocol.on_shutdown()

    def on_disconnect(self):
        self.protocol.on_disconnect()

    def __repr__(self):
        return "<Stream %s #%04x>" % (self.name, id(self) & 0xffff,)


class Protocol(object):

    stream_class = Stream
    read_size = CHUNK_SIZE

    @classmethod
    def build_stream(cls, *args, **kwargs):
        stream = cls.stream_class()
        stream.set_protocol(cls(*args, **kwargs))
        return stream

    def on_receive(self, buf):
        raise NotImplementedError

    def on_transmit(self):
        raise NotImplementedError

    def on_shutdown(self):
        raise NotImplementedError

    def on_disconnect(self):
        raise NotImplementedError

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            self.stream and self.stream.name,
        )


class Waker(Protocol):

    broker_shutdown_msg = (
        "An attempt was made to enqueue a message with a Broker that has "
        "already exitted. It is likely your program called Broker.shutdown() "
        "too early."
    )

    def __init__(self, broker):
        self.broker = broker
        self._defferred = collections.deque()

    @classmethod
    def build_stream(cls, broker):

        stream = super(Waker, cls).build_stream(broker)
        stream.accept(*os.pipe())

        return stream

    def on_receive(self, buf):
        while True:
            try:
                func, args, kwargs = self._defferred.popleft()
            except IndexError as e:
                return
            try:
                func(*args, **kwargs)
            except Exception as e:
                self.broker.shutdown()

    def on_transmit(self):
        pass

    def on_shutdown(self):
        _v and LOG.debug('%r: shutting down', self)
        self.on_disconnect()

    def on_disconnect(self):
        LOG.debug('%r: disconnecting', self)
        self.broker.stop_receive(self.stream)
        self.stream.close()

        self.stream.receive_side.close()
        if self.stream.transmit_side:
            self.stream.transmit_side.close()

    def defer(self, func, *args, **kwargs):
        self._defferred.append((func, args, kwargs))
        self._wake()

    def _wake(self):
        self.stream.write(b' ')


class BufferedWriter:

    def __init__(self, broker, protocol):
        self.broker = broker
        self.protocol: Protocol = protocol
        self._buf = collections.deque()
        self._len = 0

    def write(self, s):
        if not self._len:
            try:
                n = self.protocol.stream.write(s)
                if n:
                    if n == len(s):
                        return
            except OSError:
                pass
            self.broker._start_transmit(self.protocol.stream)
        self._buf.append(s)
        self._len += len(s)

    def on_transmit(self):
        if self._buf:
            buf = self._buf.popleft()
            written = self.protocol.stream.write(buf)
            self._len -= written

    def on_receive(self, buf):
        pass


class BootstrapProtocol(Protocol):

    def __init__(self, broker):
        self.broker = broker
        self._writer = BufferedWriter(broker, self)

    def on_transmit(self, broker):
        self._writer.on_transmit()


class Poller:

    _generation = 1
    select_class = DefaultSelector

    def __init__(self):
        self._rfds = {}
        self.select = self.select_class()

    def start_receive(self, fd: int, data=None):
        self._rfds[fd] = (data or fd, self._generation)
        self.select.register(fd, EVENT_READ, self._rfds[fd])

    def stop_receive(self):
        self._rfds.pop(fd, None)
        self.select.unregister(fd)

    def poll(self):
        self._generation += 1
        events = self.select.select()
        for key, mask in events:
            yield key.data

    def _update(self):
        pass


class Broker():

    poller_class = Poller

    def __init__(self):
        self._alive = True
        self._exitted = False
        self._waker = Waker.build_stream(self)

        self._poller = self.poller_class()
        self._poller.start_receive(
            fd=self._waker.rfd,
            data=(self._waker.on_receive, self._waker)
        )

        self._thread = threading.Thread(target=self._broken_main)
        self._thread.start()

        self.defer = self._waker.protocol.defer

    def _broken_main(self):
        while self._alive:
            self._loop_once()
        self._broker_shutdown()
        self._alive = False
        self._exitted = True
        self._broker_exit()

    def _broker_shutdown(self):
        pass

    def _broker_exit(self):
        pass

    def _loop_once(self):
        for (func, stream), _ in self._poller.poll():
            func()

    def start_receive(self, stream: Stream):
        self.defer(self._poller.start_receive, self._waker.rfd, (stream.on_receive, stream))

    def stop_receive(self, stream: Stream):
        pass

    def shutdown(self):
        pass


class PopenProcess:

    def __init__(self, proc: Popen, stdin: int, stdout: int, stderr: int):
        self.proc = proc
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr


class Message:

    def __init__(self):
        self.dst_id = None
        self.src_id = None
        pass


class IdAllocator:

    BLOCK_SIZE = 1000

    def __init__(self, router):
        self.router = router
        self.next_id = 1
        self.lock = threading.Lock()
        router.add_handler(
            fn=self.on_allocate_id,
            handle=ALLOCATE_ID
        )

    def allocate(self):
        self.lock.acquire()
        try:
            id = self.next_id
            self.next_id += 1
            return id
        finally:
            self.lock.release()

    def allocate_block(self):
        self.lock.acquire()
        try:
            id = self.next_id
            self.next_id += self.BLOCK_SIZE
            return id, self.next_id
        finally:
            self.lock.release()

    def on_allocate_id(self, msg: Message):
        id, last_id = self.allocate_block()
        msg.relay((id, last_id))


class ChildIdAllocator:

    def __init__(self, router):
        self.router = router
        self.lock = threading.Lock()
        self.it = iter(range(0))

    def allocate(self):
        self.lock.acquire()
        for id in self.it:
            return id

        master = self.router._context_by_id(0)

        self.lock.release()
        return self.allocate()


class Context():

    def __init__(self, router, context_id, name=None):
        self.router = router
        self.context_id = context_id
        self.name = name

    def send(self, msg: Message):
        msg.dst_id = self.context_id
        self.router.route(msg)
        return None

    def send_async(self, msg: Message):

        return None

    def send_await(self, msg: Message):
        self.send_async(msg)
        return None

    def __repr__(self):
        return 'Context( % r, % r)' % (self.context_id, self.name, )


class Connection():

    name_prefix = u'local'

    stream_protocol_class = BootstrapProtocol

    def __init__(self, router, options=None):
        self._router = router

    def _first_stage():
        R, W = os.pipe()
        r, w = os.pipe()
        if os.fork():
            os.dup2(0, 100)
            os.dup2(R, 0)
            os.dup2(r, 101)
            os.close(R)
            os.close(r)
            os.close(W)
            os.close(w)
            if sys.platform == 'darwin' and sys.executable == '/usr/bin/python':
                sys.executable += sys.version[:3]
            os.environ['ARGV0'] = sys.executable
            os.execl(sys.executable, sys.executable + '(mitogen:CONTEXT_NAME)')
        os.write(1, 'MITO000\n'.encode())
        C = _(os.fdopen(0, 'rb').read(1024), 'zip')
        fp = os.fdopen(W, 'wb', 0)
        fp.write(C)
        fp.close()
        fp = os.fdopen(w, 'wb', 0)
        fp.write(C)
        fp.close()
        os.write(1, 'MITO001\n'.encode())
        os.close(2)

    def _complete_connect(self):
        return

    def get_boot_command(self):
        source = inspect.getsource(self._first_stage)
        source = textwrap.dedent('\n'.join(source.strip().split('\n')[2:]))
        source = source.replace('    ', '\t')
        source = source.replace('CONTEXT_NAME', self.get_default_remote_name())
        # preamble_compressed = self.get_preamble()
        # source = source.replace('PREAMBLE_COMPRESSED_LEN',
        #                         str(len(preamble_compressed)))
        # compressed = zlib.compress(source.encode(), 9)
        encoded = base64.b64encode(source.encode())
        return ['/usr/bin/python'] + [
            '-c',
            'import base64,os,sys;exec(base64.b64decode("%s").decode())' % encoded
        ]

    def get_default_remote_name(self):
        s = u'%s@%s:%d'
        s %= (getpass.getuser(), socket.gethostname(), os.getpid())
        # In mixed UNIX/Windows environments, the username may contain slashes.
        return s.translate({
            ord(u'\\'): ord(u'_'),
            ord(u'/'): ord(u'_')
        })

    def _get_name(self):
        return u'%s.%s' % (self.name_prefix, self.proc.proc.pid)

    def _config_stdio_stream(self):
        stream = self.stream_protocol_class.build_stream(self._router.broker)
        stream.accept(self.proc.stdin, self.proc.stdout)
        stream.name = self._get_name()
        self._router.broker.start_receive(stream)
        return stream

    def start_child(self, args):
        parent_rfd, child_wfd = os.pipe()
        child_rfd, parent_wfd = os.pipe()
        stderr_r, stderr = os.pipe()
        try:
            proc = Popen(
                args=args,
                shell=True,
                stdin=child_rfd,
                stdout=child_wfd,
                stderr=None
            )
        except Exception as e:
            os.close(parent_rfd)
            os.close(child_wfd)
            os.close(parent_wfd)
            os.close(child_rfd)
            raise
        os.close(child_rfd)
        os.close(child_wfd)

        return PopenProcess(proc, parent_wfd, parent_rfd, None)

    def _async_connect(self):
        args = self.get_boot_command()
        self.proc = self.start_child(args)
        self.stdio_stream = self._config_stdio_stream()
        if self.context.name is None:
            self.context.name = self.stdio_stream.name
        self.proc.name = self.context.name

    def connect(self, context: Context):
        self.context = context
        self._router.broker.defer(self._async_connect)


class Router:

    context_class = Context

    def __init__(self):
        self.broker = Broker()
        self._context_by_id = {}
        self._stream_by_id = {}
        self._handle_map = {}
        self.id_allocator = IdAllocator(self)

    def _async_route(self, msg: Message):
        out_stream = self._stream_by_id.get(msg.dst_id)

    def add_handler(self, fn, handle):
        self._handle_map[handle] = fn

    def route(self, msg: Message):
        self.broker.defer(self._async_route, msg)

    def allocate_id():
        return self.id_allocator.allocate()

    def connect(self, method_name, **kwargs):

        context_id = self.id_allocator.allocate()
        context = self.context_class(
            router=self,
            context_id=context_id,
            name=kwargs.get('name', None)
        )

        module = __import__('remote.' + method_name, None, None, [''])
        connection: Connection = module.Connection(self)

        return connection.connect(context)

    def local(self):
        self.connect('local')
