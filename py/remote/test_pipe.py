import os
import subprocess
import time
import inspect
import textwrap

parent_rfd, child_wfd = os.pipe()
child_rfd, parent_wfd = os.pipe()

def hello():
    print('hello, the world')

source = inspect.getsource(hello)
source = textwrap.dedent(source)
source = source.replace('    ', '\t')


proc = subprocess.Popen(
    # args=['python', '-c', 'print("%s")' % source],
    args=['python'],
    stdin=child_rfd,
    # stdout=child_wfd,
    shell=True
)

# time.sleep(0.5)
os.write(parent_wfd, b'import os;\ndata = os.read(0, 1024);\nprint(data)')
os.write(parent_wfd, b'hello')

# stdout, stderr = proc.communicate()
# proc.wait()

# print(stdout)
# print(stderr)
