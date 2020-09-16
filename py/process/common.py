import logging
import tempfile

loger_name = 'test'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s,%(msecs)03d %(message)s', datefmt='%H:%M:%S')
vlog = logging.getLogger(loger_name)

# create file handler

log_path = tempfile.gettempdir() + '/test.log'
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

vlog.addHandler(fh)

print("i'm common")
