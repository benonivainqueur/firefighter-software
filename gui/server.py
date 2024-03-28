# create a simple server 

import socket
import threading
import sys
import time
from datetime import datetime

class Server:
    def __init__(self):
        self.host = "192.168.0.30"
        self.port = 12345
        self.server = None
        self.clients = []
        self.start()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print("Server is listening on port ", self.port)
        self.accept_clients()

    def accept_clients(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            print(f"Connection from {addr} has been established!")
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self, client):

        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                # print(f"Received data: {data.decode()}")
                # print("current time: ", time.ctime())
                client_side_time = data.decode().split("Current Time: ")[1]
                print("Client side time: ", client_side_time)
                # print("Time difference: ", time.ctime() - client_side_time)
                # print("time now", str(time.time()))
                print("delta ", time.time() - float(client_side_time), "seconds")
                for c in self.clients:
                    if c != client:
                        c.send(data)
            except Exception as e:
                print(e)
                break

    def close(self):
        for c in self.clients:
            c.close()
        self.server.close()
        sys.exit()

    def calculate_time_diff(server_time, client_time):
        # calculate the time difference and latency with the most accuracy possible 
        # turn server time into milliseconds
        server_time = time.mktime(server_time)
        # turn client time into milliseconds
        client_time = time.mktime(client_time)
        # calculate the difference
        diff = server_time - client_time
        return diff

if __name__ == "__main__":
    server = Server()

