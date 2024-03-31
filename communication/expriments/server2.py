import socket
import subprocess
import threading
import json
import os
from time import sleep

# Global dictionary to store client connections and their addresses
client_connections = {}
recieving = False
connected = False
lock = threading.Lock()  # Define a lock object
command = ''

def clean_fping_data(data):
    pass

def clean_iperf_data(data):
    # ping_index = data.find("PING")
        
    # json_string = data[:ping_index]
    # ping = data[ping_index:]
    json_string = json_string.replace("\\n", "")
    json_string = json_string.replace("\\t", "")
    json_string = json_string.replace("\\", "")
    json_string = json_string[1:]
    # print("CLEANED JSON:", json_string)
    
    json_data = json.loads(json_string)
    client_id = json_data["start"]["connected"][0]["local_host"][-1]
    print("client_id:", client_id)

    num_files = len([f for f in os.listdir("./data/pi" + client_id) if f.endswith('.json')])

    with open("./data/pi" + client_id + "/data" + str(num_files) + ".json", "w") as f:
        json.dump(json_data, f, indent=4)
    # with open("./data/pi" + client_id + "/ping" + str(num_files) + ".txt", "w") as f:
    #     f.write(ping)
    print("{client_id} file#{num_files} written to fs")



def clean_json(data):
    # remove [START] and [END] from data
    # fping = data.find("PING")
    is_fping = False
    # if ping index is not found, return
    if "64 bytes" in data:
        is_fping = True
    print("within clean_json..., current command is:", command)
    if is_fping:
        clean_fping_data(data)
    is_iperf = "remote_port" in command
    if is_iperf:
        clean_iperf_data(data)

   
    return data

def handle_client(connection, client_address):
    global recieving, connected
    try:
        print("Connection established with", client_address)

        client_connections[connection] = client_address
        connected = True
        data = ""
        recieving = False
        while True:
            message = connection.recv(1024).decode()
            if not message:
                break
            if "[START]" in message:
                recieving = True
                print("Recieving data from client")
                data += message
            if recieving:
                data += message
            if "[END]" in message:
                data += message
                data = data.replace("[START]", "")
                data = data.replace("[END]", "")
                clean_json(data)
                data = ""
                recieving = False


    except Exception as e:
        print(f"Error handling client connection: {e}")

def input_thread():
    global recieving, connected

    while True:
        with lock:
            sleep(0.5)
            # print("are we connected?", connected)
            # print("are we receiving?   ", recieving)
            if not recieving and connected:
                command = input("Enter command to broadcast: \n")
                broadcast_command(command)

def broadcast_command(command):
    print(f"Broadcasting {command} to {[x[1] for x in client_connections.items()]} ")
    for connection, client_address in client_connections.items():
        print(f"Client address: {client_address}")
        try:
            connection.sendall(f"{command}\n".encode())
        except Exception as e:
            print(f"Error sending command to {client_address}: {e}")

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows to reuse address 

    server_address = ('172.27.0.0', 12345)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Server is listening for incoming connections...")

    try:
        input_thread_handle = threading.Thread(target=input_thread)
        input_thread_handle.start()

        while True:
            print("Waiting for a connection...")
            connection, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
            client_thread.start()

    except Exception as e:
        print(f"Error in server: {e}")
        server_socket.close()
        return 1

    finally:
        print("Closing server socket...")
        for connection in client_connections.keys():
            print("closing connection", connection)
            connection.close()

        server_socket.close()
        return 0

if __name__ == "__main__":
    try:
        if server() == 1:
            print("Retrying...")
    except Exception as e:
        print(f"Error in server: {e}")
    finally:
        print("Closing server socket...")
        exit()
