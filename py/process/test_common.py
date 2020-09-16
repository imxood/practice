import logging
import tempfile


class MyStreamHandler(logging.StreamHandler):

    def __init__(self, stream=None):
        super().__init__(stream)

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            # issue 35046: merged two stream.writes into one.
            stream.write(msg)
            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)


# console handler
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter('%(asctime)s,%(msecs)03d  %(message)s'))

logging.basicConfig(level=logging.INFO,
                    format='%(message)s',
                    handlers=[console],
                    datefmt='%H:%M:%S')

# file handler
log_path = tempfile.gettempdir() + '/test.log'
fileHandler = logging.FileHandler(log_path, 'w')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logging.Formatter('%(message)s'))

# for test
loger_name = 'test'
vlog = logging.getLogger(loger_name)

# vlog.addHandler(console)
# vlog.addHandler(fileHandler)


def get_logger(logger_name, logfile):
    pass
