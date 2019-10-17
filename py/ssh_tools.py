
import os
import sys
from paramiko import SSHClient, AutoAddPolicy
import time
import logging
import threading
from contextlib import contextmanager


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


class Runner:

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
            yield data.decode('utf-8', "replace")

    def write_our_output(self, stream, string):
        stream.write(string)
        stream.flush()

    def _handle_output(self, buffer_, hide, output, reader):
        for data in self.read_proc_output(reader):
            if not hide:
                self.write_our_output(stream=output, string=data)
            buffer_.append(data)

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
        self.channel.close()


class RemoteShell:

    def __init__(self, hostname='127.0.0.1', port=22, username='root', password=None, log=None):

        self.connect_kwargs = dict(
            hostname=hostname,
            port=port,
            username=username,
            password=password
        )

        self.log = log if log is not None else logging.getLogger(__name__)
        self.command_cwds = list()

    def __enter__(self):

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.transport = None
        self._sftp = None

        self.client.connect('127.0.0.1', port=2222, username='root')

        self.log.debug('ssh shell __enter__')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.log.debug('ssh shell __exit__')

    def _open(self):
        if self.is_connected:
            return
        self.client.connect(**self.connect_kwargs)
        self._transport = self.client.get_transport()

    @contextmanager
    def cd(self, path):
        self.command_cwds.append(path)
        try:
            yield
        finally:
            self.command_cwds.pop()

    @property
    def sftp(self):
        self._open()
        if self._sftp is None:
            self._sftp = self.client.open_sftp()
        return self._sftp

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

    def put(self, local_file='', remote_file='', recursive=False):
        try:
            self.sftp.put(local_file, remote_file)
            self.log.debug("transfer successed!")
            return (0, 'transfer successed!', '')
        except IOError as e:
            self.log.debug('transfer failed! {}'.format(e))
            return (-1, 'transfer failed!', '')

    def run(self, cmd, hide=False):

        self._open()

        command = self._prefix_commands(cmd)

        channel = self.client.get_transport().open_session()

        remote = Remote()
        remote.start(command, channel)

        thread_args = dict()

        output = []
        error = []

        thread_args[remote.handle_stdout] = {
            'buffer_': output,
            'hide': hide,
            'output': sys.stdout
        }

        thread_args[remote.handle_stderr] = {
            'buffer_': error,
            'hide': hide,
            'output': sys.stderr
        }

        for target, kwargs in thread_args.items():
            t = ExceptionHandlingThread(target=target, kwargs=kwargs)
            t.start()

        while True:
            if remote.process_is_finished:
                break
            time.sleep(0.01)

        return (remote.returncode, ''.join(output), ''.join(error))

    @property
    def is_connected(self):
        return self.transport.active if self.transport else False

    def close(self):
        if self.is_connected:
            self.client.close()

    def _prefix_commands(self, command):
        return 'cd {} && {}'.format(self.cwd, command)


def test():

    with RemoteShell() as s:
        s.run('ls -al')
        with s.cd('test1'):
            s.run('ls -al')
            with s.cd('test2'):
                s.run('ls -al')
                with s.cd('test3'):
                    s.run('ls -al', hide=True)
        s.run('dmesg')
        # s.sftp.mkdir('test1_1')


if __name__ == "__main__":

    test()
