import os
import threading
import re


class LogPipe(threading.Thread):

    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.daemon = False
        self.logger = logger
        self.read_fd, self.write_fd = os.pipe()
        self.stop = threading.Event()
        self.start()

    def fileno(self):
        return self.write_fd

    def run(self):
        self.logger("Logging thread started.")
        with os.fdopen(self.read_fd) as f:
            for line in iter(f.readline, ""):
                line = re.sub(r'^\d+/\d+/\d+ \d+:\d+:\d+ ', '', line)
                self.logger(line.strip())
                if self.stop.is_set():
                    break
        self.logger("Logging thread finished.")

    def close(self):
        self.stop.set()
        f = os.fdopen(self.write_fd, "w")
        f.write("Stopping logging thread...\n")
        f.close()
