import socket
import threading
import json
import time
from firefighter_client import Firefighter
from tools import get_demo_firefighter_data
# create a set of test firefighters
firefighter1 = Firefighter(1,"John", "Building A, Floor 2" )
firefighter2 = Firefighter(2,"Sarah", "Building A, Floor 2" )
firefighter3 = Firefighter(3,"Michael", "Building A, Floor 2" )

class DataServer:
    def __init__(self):
        self.data = {
            "strength": "Excellent",
            "names": "John, Sarah, Michael",
            "locations": "Building A, Floor 2"
        }
        self.host = "127.0.0.1"
        self.port = 5555
        self.server = None

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client, addr = self.server.accept()
            print(f"Connected to {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    # def handle_client(self, client):
    #     try:
    #         while True:
    #             data = self.get_data_with_timestamp()
    #             client.sendall(data.encode())
    #             time.sleep(1)  # Simulate data update every 5 seconds
    #     except ConnectionResetError:
    #         print("Client disconnected")
    #         client.close()

    def handle_client(self, client, addr):
        try:
            while True:
                data = self.get_data_with_timestamp(addr)  # Include client address in the data
                client.sendall(data.encode())
                time.sleep(1)  # Simulate data update every 1 second
        except ConnectionResetError:
            print(f"Client {addr} disconnected")
            client.close()


    def get_data_with_timestamp(self):
        timestamp = time.time()
        data_with_timestamp = {
            "timestamp": timestamp,
            "data": self.data
        }
        return json.dumps(data_with_timestamp)

if __name__ == "__main__":
    server = DataServer()
    server.start_server()

    # in a seperate thread, simulate a firefighter client by running the firefighter_client.py file
    # t = threading.Thread(target=run_tapstrap_subprocess, args=("firefighter_client.py",))

