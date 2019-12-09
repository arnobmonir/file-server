from client import Client_Handler
import sys
import time
import pyautogui
file = open('C:/EWTSS/EWSSDirectory/ServerAddress_FileServer.txt', 'r')
ip_address = file.readline()
ip = "".join(ip_address.split())
try:
    client = Client_Handler(host=ip, root='C:\\')
    client.syn()
except Exception as e:
    error_code = type(e).__name__
    pyautogui.alert(text="Can't Connected to the server, Please check the server address in C: \EWTSS\EWSSDirectory\ServerAddress_FileServer.txt",
                    title=error_code, button='Exit')
