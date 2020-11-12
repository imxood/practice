## paramiko python的ssh客户端

    from paramiko import SSHClient, AutoAddPolicy

    connect_kwargs = dict(
        hostname=hostname,
        port=port,
        username=username,
        timeout=timeout,
    )
    if password:
        connect_kwargs['password'] = password

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    client.connect(**connect_kwargs)
    transport = client.get_transport()

    # open channel
    channel = transport.open_session()

    # set exec_command's timeout
    channel.settimeout(timeout)

    # set stderr --> stdout
    channel.set_combine_stderr(True)

    # exec command
    channel.exec_command('ls')

    ... channel.recv ...
