import os
import sys
import asyncio
import stat
import tempfile
import logging
import tarfile
import io
from pathlib import Path

from paramiko import SSHClient, AutoAddPolicy

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s]    %(message)s')


class Remote():

    def __init__(self, username, password=None, hostname='127.0.0.1', port=22, timeout=1, log=logging.getLogger()):

        self.command_cwds = list()
        self.log = log

        self.connect_kwargs = dict(
            hostname=hostname,
            port=port,
            username=username,
            timeout=timeout,
        )
        if not password:
            self.connect_kwargs['password'] = password

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.transport = None
        self.is_opened_sftp = False
        self.iswindows = False

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        if self.is_connected:
            return
        self.client.connect(**self.connect_kwargs)
        self.transport = self.client.get_transport()

        if not self.isdir('/tmp'):
            self.iswindows = True

    def close(self):
        if self.is_connected:
            self.client.close()
            self.transport = None

    @property
    def is_connected(self):
        return self.transport.active if self.transport else False

    @property
    def sftp(self):
        self.open()
        if not hasattr(self, '_sftp') or getattr(self, '_sftp') is None:
            self._sftp = self.client.open_sftp()
        return self._sftp

    @property
    def cwd(self):

        if not self.command_cwds:
            self.command_cwds.append(self.sftp.getcwd())

        # get the index for the subset of paths starting with the last / or ~
        for i, path in reversed(list(enumerate(self.command_cwds))):
            if not isinstance(path, str):
                return ""
            if path.startswith("~") or path.startswith("/"):
                break
        paths = [path.replace(" ", r"\ ") for path in self.command_cwds[i:]]
        return os.path.join(*paths)

    def _get_lines(self, stringio, text: str, terminator='\n'):
        pos = stringio.tell()
        if pos != 0:
            stringio.write(text)
            text = stringio.getvalue()
            stringio.seek(0)
            stringio.truncate()
        lines = text.split(terminator)
        if lines[-1] != '':
            stringio.write(lines[-1])
            return lines[:-1]
        else:
            stringio.seek(0)
            stringio.truncate()
            return lines

    async def recv(self, deal_func, num_bytes, hide, bufferQ, terminator='\n'):
        buffer = io.StringIO()
        while True:
            # if the data is empty, the transmission ends
            data = deal_func(num_bytes)
            if not data:
                break
            data = data.decode('utf-8', "replace")
            lines = self._get_lines(buffer, data)
            for line in lines:
                if line:
                    if bufferQ:
                        await bufferQ.put(line + terminator)
                    if not hide:
                        self.log.info(line)
            # if len(lines) > 1 and lines[-1] == '':
            #     self.lastline = lines[-2]
        return data

    async def run(self, cmd, hide=False, timeout=None, bufferQ: asyncio.Queue = None, num_bytes=1024):
        self.open()
        command = self._prefix_commands(cmd)
        # open channel
        channel = self.transport.open_session()
        # set exec_command's timeout
        channel.settimeout(timeout)
        # exec command
        channel.exec_command(command)
        # wait the task's output
        output_task = asyncio.ensure_future(
            self.recv(channel.recv, num_bytes, hide, bufferQ))
        output_err_task = asyncio.ensure_future(
            self.recv(channel.recv_stderr, num_bytes, hide, bufferQ))
        output, output_err = await asyncio.gather(output_task, output_err_task)
        # get tha command return code
        retcode = channel.recv_exit_status()
        # close channel
        channel.close()
        return (retcode, output, output_err)

    def isdir(self, path):
        """ judge if the remote path existes """
        try:
            return stat.S_ISDIR(self.sftp.stat(path).st_mode)
        except IOError:
            return False

    def mkdir(self, path):
        """ it need is '/' path if the path is multilevel"""
        """ the path look like c:/a/b/c below windows """
        if self.isdir(path):
            raise Exception('the directory specified already exists: ' + path)
        try:
            dirs = path.split('/')
            dir = dirs.pop(0)
            while True:
                if not self.isdir(dir):
                    self._sftp.mkdir(dir)
                if len(dirs) == 0 or len(dirs) == 1 and dirs[0].strip() == '':
                    return
                dir = dir + '/' + dirs.pop(0)
        except Exception as e:
            raise e

    def rm(self, path):
        """ delete remote file, not a dir """
        if self.exists(path) and not self.isdir(path):
            self._sftp.remove(path)

    def rm_dir(self, path):
        """ delete remote dir, not a file """

        if self.exists(path):

            files = self._sftp.listdir(path=path)

            for f in files:
                filepath = '{}/{}'.format(path, f)
                if self.isdir(filepath):
                    self.rm_dir(filepath)
                else:
                    self._sftp.remove(filepath)
            self._sftp.rmdir(path)

    def put(self, local_file, remote):
        """ upload local file to remote, is local file, not a local dir!! """

        ori_local = local_file
        if not os.path.isabs(local_file):
            local_file = os.path.join(os.getcwd(), local_file)

        if not os.path.exists(local_file):
            self.log.error('local file "{}" doesn\'t exist.'.format(ori_local))
            return False

        try:
            if self.isdir(remote):
                remote = os.path.join(remote, os.path.basename(local_file))
            self._sftp.put(local_file, remote)
            self.log.info(
                '[local file] {} --> [remote file] {}'.format(local_file, remote))
            return True
        except IOError as e:
            self.log.error('transfer failed! err: {}'.format(e))
            return False

    def put_dir(self, local_dir, dest_dir):
        """ upload local dir to remote, is local dir, not a local file!! """

        target_dir = Path(dest_dir, Path(local_dir).name)

        if self.exists(target_dir.__str__()):
            self.rm_dir(target_dir.__str__())

        local_tar_file = Path(tempfile.gettempdir(),
                              os.path.basename(local_dir) + '.tar.gz')
        if local_tar_file.exists():
            os.remove(local_tar_file)

        self.__make_targz(local_dir, local_tar_file)

        remote_tar_file = Path(dest_dir, local_tar_file.name).__str__()

        self.put(local_tar_file, remote_tar_file)
        self.run('python3 -m tarfile -e {} {}'.format(remote_tar_file, dest_dir))
        self.rm(remote_tar_file)

        os.remove(local_tar_file)

        self.log.info(
            '[local dir] {} --> [remote file] {}'.format(local_dir, dest_dir))

        return True

    def exists(self, path):
        """judge whether the remote path existes
        """
        try:
            self.sftp.stat(path)
        except IOError as e:
            if 'No such file' in str(e):
                return False
            raise
        else:
            return True

    def __make_targz(self, local_dir, output_filename):
        with tarfile.open(output_filename, 'w:gz') as tar:
            tar.add(local_dir, arcname=os.path.basename(local_dir))

    def _prefix_commands(self, command):
        cwd = self.cwd
        if cwd:
            return 'cd {} && {}'.format(self.cwd, command)
        return command


console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter('%(asctime)s [%(name)s]    %(message)s'))

fileHandler = logging.FileHandler(tempfile.gettempdir() + '/test.log', 'w')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logging.Formatter('%(message)s'))

slog = logging.Logger('serial')
slog.addHandler(console)
slog.addHandler(fileHandler)

tlog = logging.getLogger()


async def serial_task():

    bufferQ = asyncio.Queue()

    with Remote('maxu', log=slog) as r:

        tlog.info('serial ...')

        command = 'plink -serial /dev/ttyUSB0 -sercfg 115200,8,n,1,N'

        task = asyncio.ensure_future(r.run(command, bufferQ=bufferQ))

        while True:
            try:
                line = await asyncio.wait_for(bufferQ.get(), timeout=10)
                tlog.info(line)
            except asyncio.QueueEmpty:
                await task.cancel()
                break
        return 0


async def main():
    with Remote('maxu', log=slog) as r:
        ret = await r.run('ls -al')
        print(ret)
    await serial_task()


if __name__ == "__main__":
    asyncio.run(main())
