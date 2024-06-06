import sys

class Logger:
    def __init__(self, log_file_path):
        self.log_file = open(log_file_path, 'w')
        self.terminal = sys.stdout

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)
        self.flush()  # Ensure message is immediately written to both log and console

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        self.log_file.close()

def setup_logger(log_file_path):
    logger = Logger(log_file_path)
    sys.stdout = logger
    sys.stderr = logger
    return logger
