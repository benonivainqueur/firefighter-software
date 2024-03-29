# create a simple client 

import socket
import threading
import sys
from datetime import datetime
import time
import os
# 192.168.0.71
class Client:
    def __init__(self):
        self.host = "192.168.0.30"
        self.port = 12345
        self.client = None
        # self.client_id = os.environ.get("PI_ID")
        self.client_id = "1"
        self.start()

    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print("Connected to server")
        self.send_message()
    def get_client_id(self):
        # get the system variable $PI_ID
        return self.client_id
        # return self.client.fileno()


    def send_message(self):
        while True:
            time.sleep(2)
            # message = input("Enter message: ")
            message = "Client #{} ".format(self.get_client_id())
            message += "Current Time: " + str(time.time())
            self.client.send(message.encode())
            # if message == "exit":
            #     break

    def close(self):
        self.client.close()
        sys.exit()

if __name__ == "__main__":
    client = Client()
# ```
# Path: gui/server.py