#!/usr/bin/env python3

import os
import os.path as path
import configparser as cp
import paramiko
import getpass


script_path = path.abspath(path.dirname(__file__))

config_file = path.join(script_path, 'test.conf')

def ssh_connect(host, port, username, password):

    try:

        ssh_fd = paramiko.SSHClient()
        ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_fd.connect(host, port, username, password)

    except Exception as e:
        print('ssh {}@{}: {}'.format(username, host, e))
        exit(-1)

    return ssh_fd

def ssh_exec(ssh_fd, cmd):

    stdin, stdout, stderr = ssh_fd.exec_command(cmd)
    # for line in iter(stdout.readline, b''):
    #     print(line)
    result = stdout.read().decode()
    if result:
        return (0, result)

    result = stderr.read().decode()
    if result:
        return (0, result)

    print('error: reach an inaccessible place.')

def ssh_disconnect(ssh_fd):
    ssh_fd.close()



config = cp.ConfigParser()
config.read(config_file)

ssh_fd = ssh_connect(host, port, username, password)

ret = ssh_exec(ssh_fd, "ls -al")

print(ret[0])
print(ret[1])
