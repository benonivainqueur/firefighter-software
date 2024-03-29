import socket
import json
import os
from datetime import datetime

def send_command_to_nodes(command, nodes, server_socket):
    # each node is a dictory with keys: name, ip, port
    for node in nodes:
        try:
            print("in send_command_to_nodes")
            print(f"Sending command to {node[0]}:{node[1]}")
        
            # server_socket.sendto(command.encode(), (node[0], node[1]))
            server_socket.send(command.encode())


        except Exception as e:
            print(f"Error: {e}")

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
    # server_ip = '172.27.0.0'  # Listen on all available interfaces
    server_ip = '192.168.0.30'  # Listen on all available interfaces

    server_port = 12345  # Server's port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server IP address and port
    server_socket.bind((server_ip, server_port))

    # Listen for incoming connections (up to 5 clients)
    server_socket.listen(5)
    print("Server is listening for incoming connections...")
    nodes = {}
    # [("mbp", "192.168.0.30", 12345),
    #         ("pi1", "172.27.0.1", 12345),
    #         ("pi2", "172.27.0.2", 12345), 
    #         ("pi3", "172.27.0.3", 12345),
    #         ("pi4", "172.27.0.4",   12345),
    #         ("pi5", "172.27.0.5",   12345),]
    # nodes = {
    #     # "mbp": {"ip": "192.168.0.30", "port": 12345},

    # }
    nodes = [("192.168.0.30", 12345)]
    nodes = []
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")
    nodes.append((client_address[0], 12345))
    # when a new node connected

    while True:
        client_socket, client_address = server_socket.accept()
        # Accept incoming connection
        


        
        # nodes = {}
        # add the new node to the dictionary
        # get the name of the node depending on the ip address
        # name = "unknown"
        
        
        # add the new node to the dictionary 

          
        command = input("Enter command (e.g., 'iperf3 -c server_ip -t 10'): ")
        try:
            send_command_to_nodes(command, nodes, client_socket)

            # Receive data from client
            received_data = client_socket.recv(4096).decode("utf-8")
            print("Data received:", received_data)
            # Parse received JSON data
            # client_data = json.loads(received_data)

            # Save received data to files
            # save_data_to_files(client_data, client_address[0])

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the client socket
            client_socket.close()

    # Close the server socket
    server_socket.close()

if __name__ == "__main__":
    main()
