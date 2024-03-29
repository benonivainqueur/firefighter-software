import socket
import json
import os
from datetime import datetime

def send_command_to_nodes(command, nodes):
    for node in nodes:
        try:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the node
            client_socket.connect((node['ip'], node['port']))

            # Send command to the node
            client_socket.sendall(command.encode())

            # Close the connection
            client_socket.close()

        except Exception as e:
            print(f"Error sending command to node {node['ip']}: {e}")

# Function to save received data to files
def save_data_to_files(data, client_address):
    # Create a folder with the current date and time
    folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("./data/"+folder_name, exist_ok=True)

    # Save each client's data to a separate file within the folder
    for ip_address, client_data in data.items():
        file_name = os.path.join(folder_name, f"{client_data['name']}.json")
        with open(file_name, "w") as file:
            json.dump(client_data, file)
        print(f"Data from {ip_address} saved to file: {file_name}")

def main():
    # Define server IP address and port
    server_ip = '172.27.0.0'  # Listen on all available interfaces
    server_port = 12345  # Server's port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server IP address and port
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections (up to 5 clients)
    server_socket.listen(5)
    print("Server is listening for incoming connections...")
    nodes = [("pi1", "172.27.0.1"),
            ("pi2", "172.27.0.2"), 
            ("pi3", "172.27.0.3"),
            ("pi4", "172.27.0.4"),
            ("pi5", "172.27.0.5")]

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        command = input("Enter command (e.g., 'iperf3 -c server_ip -t 10'): ")
        send_command_to_nodes(command, nodes)
        try:
            # Receive data from client
            received_data = client_socket.recv(4096).decode("utf-8")

            # Parse received JSON data
            client_data = json.loads(received_data)

            # Save received data to files
            save_data_to_files(client_data, client_address[0])

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the client socket
            client_socket.close()

    # Close the server socket
    server_socket.close()

if __name__ == "__main__":
    main()
