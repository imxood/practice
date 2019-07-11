import os
import re

data = 'Default \x1b[91mLight red, Default \x1b[93mLight yellow, Default \x1b[92mLight green\x1b[0m'
print(data)

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

# data = b'\x1b[0m<inf> encoder_run: counter: 2205\x1b[0m\r\n'
# data = data.decode().rstrip()

data = ansi_escape.sub('', data)

print(data)
