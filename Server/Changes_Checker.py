import time
import threading
from Server_Logger import Server_Logger


class Checker(threading.Thread):
    def __init__(self, server_address, log_address, log_time):
        self.server_address = server_address
        self.log_address = log_address
        self.log_time = log_time

        threading.Thread.__init__(self)

    def run(self):
        while True:
            server_logger = Server_Logger(
                self.server_address, self.log_address, self.log_time)
            time.sleep(10)
