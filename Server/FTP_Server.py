import subprocess
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer
import os
from Server_Logger import Server_Logger
import socket
import time
import threading
from Changes_Checker import Checker
import pyautogui


class FTP_SERVER:
    def __init__(self):
        path = os.getcwd()
        if path.startswith('C'):
            os.chdir('\\')
        else:
            os.chdir('C:')
        self.hose_name = socket.gethostname()
        self.ip = socket.gethostbyname(self.hose_name)
        self.port = '21'
        self.root_dir = 'C:'
        self.server_address = '\EWTSS'
        self.log_address = 'EWTSS\log\change_log_name.txt'
        self.log_time = 'EWTSS\log\change_log_time.txt'
        self.log_folder = 'EWTSS\log'
        self.server = ThreadedFTPServer
        self.changes_cheker = Checker(
            self.server_address, self.log_address, self.log_time)

    def log_generator(self):
        if os.path.exists(self.log_folder):
            server_logger = Server_Logger(
                self.server_address, self.log_address, self.log_time)
        else:
            try:
                os.makedirs(self.log_folder)
                server_logger = Server_Logger(
                    self.server_address, self.log_address)
            except Exception as e:
                print(e)

    def start(self):
        try:
            answer = pyautogui.confirm('Server will start on :: '+self.ip,
                                       "FTP Server", ("Start", "Stop"))
            if answer == "Start":
                self.log_generator()
                try:
                    self.changes_cheker.start()
                except Exception as e:
                    print(e, ":: Starting Thread")
                authorizer = DummyAuthorizer()
                authorizer.add_user('EWTSS_FTP_USER', 'EWTSS', '.')
                handler = FTPHandler
                handler.authorizer = authorizer
                self.server = ThreadedFTPServer((self.ip, self.port), handler)
                self.server.serve_forever()

        except Exception as e:
            pyautogui.alert(text=str(e), title=str(
                type(e).__name__), button='Exit')


FTP_SERVER().start()
