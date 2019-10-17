
import os
import sys
import configparser as cp
import paramiko
import getpass
import re
import time
import logging
import threading
from contextlib import contextmanager

from fabric import Connection


script_path = os.path.abspath(os.path.dirname(__file__))


def get_device_config(config_file, device_index):

    if not os.path.isfile(config_file):
        self.log.error("file[%s] didn't exist" % config_file)
        sys.exit(-1)

    config = cp.ConfigParser()
    config.read(config_file)

    sections = config.sections()

    if device_index + 1 > len(sections):
        log.error('device index error')
        log.warning('The optional device are:')
        for index, device in enumerate(sections):
            log.info('index: {}, device name: {}'.format(index, device))
        return None

    device = sections[device_index]

    return config[device]


class ExceptionHandlingThread(threading.Thread):

    def __init__(self, **kwargs):
        super(ExceptionHandlingThread, self).__init__(**kwargs)
        self.daemon = True
        self.kwargs = kwargs

    def run(self):
        try:
            if hasattr(self, "_run") and callable(self._run):
                self._run()
            else:
                super(ExceptionHandlingThread, self).run()
        except BaseException:
            # Store for actual reraising later
            self.exc_info = sys.exc_info()
            # And log now, in case we never get to later (e.g. if executing
            # program is hung waiting for us to do something)
            msg = "Encountered exception {!r} in thread for {!r}"
            # Name is either target function's dunder-name, or just "_run" if
            # we were run subclass-wise.
            name = "_run"
            if "target" in self.kwargs:
                name = self.kwargs["target"].__name__
            print(msg.format(self.exc_info[1], name))  # noqa


class Runner(object):

    read_chunk_size = 1000

    def __init__(self):
        pass

    def read_proc_stdout(self, num_bytes):
        pass

    def read_proc_stderr(self, num_bytes):
        pass

    def read_proc_output(self, reader):
        while True:
            data = reader(self.read_chunk_size)
            if not data:
                break
            yield self.decode(data)

    def write_our_output(self, stream, string):
        stream.write(encode_output(string, self.encoding))
        stream.flush()

    def _handle_output(self, buffer_, hide, output, reader):
        # TODO: store un-decoded/raw bytes somewhere as well...
        for data in self.read_proc_output(reader):
            if not hide:
                self.write_our_output(stream=output, string=data)
            # Store in shared buffer so main thread can do things with the
            # result after execution completes.
            # NOTE: this is threadsafe insofar as no reading occurs until after
            # the thread is join()'d.
            buffer_.append(data)
            # Run our specific buffer through the autoresponder framework
            self.respond(buffer_)

    def handle_stdout(self, buffer_, hide, output):
        self._handle_output(
            buffer_, hide, output, reader=self.read_proc_stdout
        )

    def handle_stderr(self, buffer_, hide, output):
        self._handle_output(
            buffer_, hide, output, reader=self.read_proc_stderr
        )


class Remote(Runner):

    def __init__(self, *args, **kwargs):
        super(Remote, self).__init__(*args, **kwargs)

    def start(self, command, channel):
        self.channel = channel
        self.channel.exec_command(command)

    def read_proc_stdout(self, num_bytes):
        return self.channel.recv(num_bytes)

    def read_proc_stderr(self, num_bytes):
        return self.channel.recv_stderr(num_bytes)

    def _write_proc_stdin(self, data):
        return self.channel.sendall(data)

    @property
    def process_is_finished(self):
        return self.channel.exit_status_ready()

    @property
    def returncode(self):
        return self.channel.recv_exit_status()

    def stop(self):
        if hasattr(self, "channel"):
            self.channel.close()


class RemoteShell:

    def __init__(self, host=None, user=None, password=None, port=None, log=None):

        self.user = user
        self.password = password
        self.host = host
        self.port = port if port is None else int(port)

        self.log = log if log is not None else logging.getLogger(__name__)

        self.command_cwds = list()

    def __enter__(self):

        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.host, self.port, self.user, self.password)

        self.sftp = paramiko.SFTPClient.from_transport(
            self.ssh_client.get_transport()
        )

        # stdin, stdout, stderr = self.ssh_client.exec_command('pwd')
        # self.path = stdout.read().decode().strip()

        self.log.debug('ssh shell __enter__')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.log.debug('ssh shell __exit__')

    @contextmanager
    def cd(where):
        self.command_cwds.append(path)
        try:
            yield
        finally:
            self.command_cwds.pop()

    @property
    def cwd(self):

        if not self.command_cwds:
            return ""

        # get the index for the subset of paths starting with the last / or ~
        for i, path in reversed(list(enumerate(self.command_cwds))):
            if path.startswith("~") or path.startswith("/"):
                break

        paths = [path.replace(" ", r"\ ") for path in self.command_cwds[i:]]
        return os.path.join(*paths)

    def get(self, remote_file='', local_file=''):
        try:
            self.sftp.get(remote_file, local_file)
            self.log.debug("transfer successed!")
            return (0, 'transfer successed!', '')
        except IOError as e:
            self.log.debug('transfer failed! {}'.format(e))
            return (-1, 'transfer failed!', '')

    def put(self, recursive, local_file='', remote_file=''):
        try:
            self.sftp.put(local_file, remote_file)
            self.log.debug("transfer successed!")
            return (0, 'transfer successed!', '')
        except IOError as e:
            self.log.debug('transfer failed! {}'.format(e))
            return (-1, 'transfer failed!', '')

    def run(self, cmd):

        command = self._prefix_commands(cmd)

        channel = self.ssh_client.get_transport().open_session()

        r = Remote()
        r.start(command, channel)

        thread_args = dict()

        output = []
        error = []

        thread_args[r.handle_stdout] = {
            'buffer_': output,
            'hide': False,
            'output': sys.stdout
        }

        thread_args[r.handle_stderr] = {
            'buffer_': error,
            'hide': False,
            'output': sys.stderr
        }

        for target, kwargs in thread_args.items():
            t = ExceptionHandlingThread(target=target, kwargs=kwargs)
            t.start()

        while True:
            if r.process_is_finished:
                break
            time.sleep(0.01)

        return (r.returncode, output, error)

        # buff_size = 10240000
        # exit_status = 0

        # channel.get_pty()

        # channel.exec_command(cmd)

        # while not channel.exit_status_ready():

        #     time.sleep(0.001)

        #     if not channel.recv_ready() and not channel.recv_stderr_ready():
        #         continue

        #     while channel.recv_ready():
        #         out = channel.recv(buff_size).decode()
        #         handle_log(out)

        #     while channel.recv_stderr_ready():
        #         out = channel.recv_stderr(buff_size).decode()
        #         handle_error_log(out)
        #         exit_status = -2

    def close(self):
        self.ssh_client.close()

    def _prefix_commands(self, command):
        if self.cwd:
            return 'cd {} && '.format(self.cwd)
        return ''


def test():

    config_file = os.path.join(script_path, 'tools/remote/config.conf')

    config = cp.ConfigParser()
    config.read(config_file)

    device_config = config['pi_dengwei']

    host = device_config['host']
    port = device_config['port']
    user = device_config['user']
    password = device_config['password']

    with RemoteShell(host, user, password, port) as s:
        s.run('ls')
        s.run('dmesg')

    # scp = RemoteScp(user, password, host, port)
    # scp.put('/home/mx/work/cvf/pse/modules/pse_validation/tools/flash.sh',
    #         '/home/pi/maxu/flash.sh.1')
    # scp.get('/home/pi/maxu/flash.sh.1',
    #         '/home/mx/work/cvf/pse/modules/pse_validation/tools/flash.sh.2')

if __name__ == "__main__":

    test()
