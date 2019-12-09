import os
import time
import datetime


class Server_Logger:
    def __init__(self, server_address, log_address, log_time):
        self.server_address = server_address
        self.log_address = log_address
        self.log_time = log_time
        self.GetAllDirectories(self.server_address)

    def clear_log_file(self, file_dir):
        if os.path.exists(file_dir):
            os.remove(file_dir)

    def write_log(self, mssg, time):
        file = open(self.log_address, "a")
        file.write(mssg + '>> \n')
        file.close()
        file = open(self.log_time, 'a')
        file.write(str(time)+'\n')

    def file_modified_time(self, file_dir):
        file_time_ex = os.path.getmtime(file_dir)
        return file_time_ex

    def GetAllDirectories(self, file_path):
        files_dir = []
        self.clear_log_file(self.log_address)
        self.clear_log_file(self.log_time)
        folder_list = os.listdir(file_path)
        for folder in folder_list:
            if not "Map" == folder and not 'log' == folder:
                for folder_dir, files, all_files in os.walk(file_path+"\\"+folder):
                    for file in all_files:
                        path = folder_dir + "\\" + file
                        self.write_log(path, self.file_modified_time(path))
