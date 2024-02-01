import tkinter as tk
from tkinter import ttk
import socket
import json

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Firefighter Dashboard")
        self.root.geometry("600x400")

        # Labels to display data
        self.strength_label = ttk.Label(root, text="Bluetooth/Wi-Fi Strength:")
        self.strength_label.pack()

        self.names_label = ttk.Label(root, text="Firefighter Names:")
        self.names_label.pack()

        self.locations_label = ttk.Label(root, text="Firefighter Locations:")
        self.locations_label.pack()

        # Connect to the server
        self.server_host = "127.0.0.1"
        self.server_port = 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

        # Start receiving data
        self.receive_data()

    def receive_data(self):
        while True:
            data = self.client_socket.recv(1024).decode()
            print("Received data:", data)
            data_dict = json.loads(data)
            self.update_labels(data_dict["data"])

    def update_labels(self, data):
        strength = data["strength"]
        names = data["names"]
        locations = data["locations"]
        self.strength_label.config(text=f"Bluetooth/Wi-Fi Strength: {strength}")
        self.names_label.config(text=f"Firefighter Names: {names}")
        self.locations_label.config(text=f"Firefighter Locations: {locations}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
