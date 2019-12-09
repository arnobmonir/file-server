import os
import time
import re
from ftplib import FTP
import datetime
import sys
import patoolib
import pyautogui
from tkinter import *
from tkinter.ttk import *


class Client_Handler:
    def __init__(self, host, root="D:\\"):
        self.root = root
        self.project_folder = "EWTSS"
        self.server_log_name = "EWTSS\log\change_log_name.txt"
        self.server_log_time = "EWTSS\log\change_log_time.txt"
        self.client_log_name = "EWTSS\log\client_log_name.txt"
        self.client_log_time = "EWTSS\log\client_log_time.txt"
        self.diff_list = []
        self.ftp = FTP(host=host)
        self.ftp.login("EWTSS_FTP_USER", 'EWTSS')
        self.Cheack_directory()
        self.roottk = Tk()
        self.roottk.overrideredirect(1)
        self.roottk.wm_attributes("-topmost", 1)
        ws = self.roottk.winfo_screenwidth()
        hs = self.roottk.winfo_screenheight()
        w = 350
        h = 50
        x = (ws / 2) - (w/2)
        y = (hs/2)-(h/2)
        self.roottk.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.mssg_val = StringVar()
        self.mssg = Label(self.roottk, textvariable=self.mssg_val)
        self.progress = Progressbar(self.roottk, orient=HORIZONTAL,
                                    length=300, mode='determinate')
        self.mssg.pack()

    def bar(self, num):
        self.progress['value'] = num
        self.roottk.update_idletasks()
        self.progress.pack(pady=5)

    def Cheack_directory(self):
        if os.path.exists(self.root+self.project_folder):
            os.chdir(self.root+self.project_folder)
            os.chdir('..')
        else:
            os.makedirs(self.root + self.project_folder)
            os.chdir(self.root+self.project_folder)
            os.chdir('..')
        if not os.path.exists(os.path.dirname(self.client_log_name)):
            os.makedirs(os.path.dirname(self.client_log_name))
            open(self.client_log_name, 'a').write('')
            open(self.client_log_time, 'a').write('')

    def clear_log_file(self, file_dir):
        if os.path.exists(file_dir):
            os.remove(file_dir)

    def write_log(self, mssg, time):
        file = open(self.client_log_name, "a")
        file.write(mssg + '>> \n')
        file = open(self.client_log_time, 'a')
        file.write(str(time) + ' \n')
        file.close()

    def file_modified_time(self, file_dir):
        file_time_ex = os.path.getmtime(file_dir)
        return file_time_ex

    def GetAllDirectories(self, file_path):
        files_dir = []
        self.clear_log_file(self.client_log_name)
        self.clear_log_file(self.client_log_time)
        for folder_dir, files, all_files in os.walk(file_path):
            for file in all_files:
                path = folder_dir + "\\" + file
                if not "EWTSS\Map\\" in path:
                    self.write_log(path, self.file_modified_time(path))

    def return_ulr_from_log(self, test_text):
        sub_string = re.findall("(EWTSS.*)(>>)", test_text)
        return sub_string[0][0]

    def txt_to_str(self, file_name):
        line_list = []
        if os.path.exists(file_name):
            file = open(file_name, "r")
            for line in file:
                line_list.append(line)
        return line_list

    def precise_data(self, logs, log_time):
        logs_dict = {}
        for index in range(0, len(logs)):
            try:
                logs_dict[logs[index]] = log_time[index]
            except Exception as e:
                print(e, 'index ', index)
        return logs_dict

    def compare_log_file(self):
        server_log_list = self.txt_to_str(self.server_log_name)
        server_log_time_list = self.txt_to_str(self.server_log_time)
        client_log_list = self.txt_to_str(self.client_log_name)
        client_log_time_list = self.txt_to_str(self.client_log_time)
        server_dist = self.precise_data(server_log_list, server_log_time_list)
        client_dict = self.precise_data(client_log_list, client_log_time_list)

        # diff_list = list(set(line_1) - set(line_2))
        for server_line in server_log_list:
            if not server_line in client_log_list:
                self.diff_list.append(server_line)
            elif server_line in client_log_list:
                if datetime.datetime.fromtimestamp(float(server_dist[server_line])) > datetime.datetime.fromtimestamp(float(client_dict[server_line])):
                    print(datetime.datetime.fromtimestamp(float(
                        server_dist[server_line])), datetime.datetime.fromtimestamp(float(client_dict[server_line])))
                    self.diff_list.append(server_line)

    def remove_previous_file(self, file_path):
        os.rename(file_path)

    def download_from_ftp(self, ftp_path):
        path = self.root + ftp_path
        try:
            if os.path.exists(os.path.dirname(ftp_path)):
                self.ftp.retrbinary(
                    'RETR ' + ftp_path, open(ftp_path, 'wb').write)
            else:
                os.makedirs(self.root+os.path.dirname(ftp_path))
                self.ftp.retrbinary(
                    'RETR ' + ftp_path, open(ftp_path, 'wb').write)
        except Exception as e:
            print(e, ftp_path)

    def log_from_ftp(self, ftp_path):

        try:
            if os.path.exists(os.path.dirname(ftp_path)):
                self.ftp.retrbinary('RETR '+ftp_path,
                                    open(ftp_path, 'wb').write)
            else:
                os.makedirs(os.path.dirname(ftp_path))
                self.ftp.retrbinary('RETR '+ftp_path,
                                    open(ftp_path, 'wb').write)
        except Exception as e:
            print(e, ftp_path)

    def run(self):
        self.compare_log_file()
        answer = 'Later'
        file_count = len(self.diff_list)
        if file_count > 0:
            answer = pyautogui.confirm('Some Updates found. Do you want to update now?',
                                       "System Update", ("Now", "Later"))
        if answer == 'Now':
            file_no = 1
            self.bar(1)
            for url in self.diff_list:
                print(url)
                bar_value = (file_no / file_count) * 100
                self.mssg_val.set(str(file_no) + " / " + str(file_count))
                try:
                    self.download_from_ftp(self.return_ulr_from_log(url))
                    file_no = file_no+1
                    self.bar(bar_value)
                except Exception as e:
                    print(e, url)
                    pass

    def extract_compress(self):
        self.mssg_val.set('Extracting Zip file...')
        for zip_url in self.diff_list:
            filename, file_extension = os.path.splitext(
                self.return_ulr_from_log(zip_url))
            if ".zip" == file_extension:

                try:
                    patoolib.extract_archive(
                        self.return_ulr_from_log(zip_url), outdir=self.root + self.project_folder + "\\Map")
                except Exception as e:
                    print(e, zip_url)

            elif ("rar" == file_extension):
                print("no module found to extract rar file")

    def syn(self):
        self.GetAllDirectories("\EWTSS")
        self.clear_log_file(self.server_log_name)
        self.log_from_ftp(self.server_log_name)
        self.log_from_ftp(self.server_log_time)
        self.run()
        self.extract_compress()
        self.roottk.quit()


# How to start this client
# example: client.py -i 192.168.100.10 -u EWTSS -p password


# Client_Handler().syn()
