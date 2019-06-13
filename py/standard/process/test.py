import os
import subprocess as sp

# command = "ls -al".split()
dir = os.path.dirname(os.path.abspath(__file__))
command = "bash %s/test.sh" % dir
print(command.split())

proc = sp.Popen(command.split(), stdout=sp.PIPE, stderr=sp.STDOUT)
proc.wait()
for line in proc.stdout:
   #the real code does filtering here
   print "test:", line.rstrip()
# print(proc.returncode)
#
