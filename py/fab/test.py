from fabric import Connection


c = Connection('mx@maxu-pc', connect_kwargs={'password': 'imxood'})

# c.put('py', '/home/mx/test')
# c.run('ls -al ~/test')

with c.cd('~'):
    c.run('pwd')

with c.cd('~/test'):
    c.run('pwd')
