import socket
import subprocess
import threading
import json
import os
from time import sleep
import re

# Global dictionary to store client connections and their addresses
client_connections = {}
recieving = False
connected = False
lock = threading.Lock()  # Define a lock object
command = ''


def clean_fping_data(data):
    print("within clean_fping data")
    client_id = data.split("\n")[0]
    # remove the , at the beginning of the client_id
    # remove everything that isnt a digit
    client_id = re.sub(r'\D', '', client_id)
    client_id = client_id[-1]
    print("client_id:", client_id)

    data = data.split("\n")[2:]
    # get unique ip addresses 
    ips = set()
    for i in range(len(data)):
        if len(data[i]) > 0:
            ips.add(data[i].split()[0])

    # print("DATA: ", data)
    # remove empty strings
    for i in range(len(data)):
        if len(data[i]) == 0:
            data.pop(i)
    dict_data = {}
    for d in data: 
        ip,xmt,rcv,loss,min,avg,max =None, None, None, None, None, None, None
        # fill array with -1 
        populated_arr = [-1,-1,-1,-1,-1,-1,-1]
        d = d.strip()
        # remove all spaces
        d = d.replace(" ", "")
        # if " min/avg/max = " in d:
        d = d.replace ("min/avg/max=", "")
        d = d.replace("%", "")
        d=d.replace(":", "")
        d = d.replace("xmt/rcv/loss=", ",")
        d = d.replace("/", ",") 
        d = d.split(",")
        for i in range(len(d)):
            populated_arr[i] = d[i]
        print(populated_arr)
        # add the populated array to the dictionary
        dict_data[populated_arr[0]] = populated_arr[1:]
    # print("DICTIONARY:", dict_data)


    result = {
        "client_id": client_id,
        "ips": list(ips),
        "data": dict_data
    }
    # /home/pi1/firefighter-software/communication/experiments/data/pi1
    client_id = client_id.strip()
    num_files = len([f for f in os.listdir("./data/pi" + client_id) if f.endswith('.json') and "ping" in f])
    with open("./data/pi" + client_id + "/ping" + str(num_files) + ".json", "w") as f:
        print("WRITING TO FILE #:", "./data/pi" + client_id + "/ping" + str(num_files) + ".json")
        f.write(json.dumps(result, indent=4))

    return json.dumps(result, indent=4)

def clean_iperf_data(json_string):
    # ping_index = data.find("PING")
    json_string = json_string[:-1]
    # json_string = data.strip
    # print("DATA:",data)
    # json_string = data[:ping_index]
    # ping = data[ping_index:]
    json_string = json_string.replace("\\t", "")
    json_string = json_string.replace("\\n", "")
    json_string = json_string.replace("\\", "")
    json_string = json_string[1:]# remove the first character
    
    # remove the last character
    # json_string = json_string[:-1]
    # json_string = data[:-1]

    print("CLEANED JSON:", json_string)
    
    json_data = json.loads(json_string)
    client_id = json_data["start"]["connected"][0]["local_host"][-1]
    print("client_id:", client_id)

    num_files = len([f for f in os.listdir("./data/pi" + client_id) if f.endswith('.json') and "iperf" in f])

    with open("./data/pi" + client_id + "/iperf" + str(num_files) + ".json", "w") as f:
        json.dump(json_data, f, indent=4)
    # with open("./data/pi" + client_id + "/ping" + str(num_files) + ".txt", "w") as f:
    #     f.write(ping)
    print(f"pi{client_id} file #:{num_files} saved")



def clean_json(data):
    # remove [START] and [END] from data
    # fping = data.find("PING")
    # is_fping = False
    # if ping index is not found, return
    is_fping = "xmt" in data
    is_iperf = "remote_port" in data
    if is_fping:
        print("cleaning fping data")
        data = clean_fping_data(data)
    # print("is iperf:", is_iperf)
    elif is_iperf:
        print("cleaning iperf data")
        # print("is iperf")
        data = clean_iperf_data(data)
    else:
        print("none of the json types detected in clean_json")


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
                # print("Recieving data from client")
                data += message
                print(data)
            if recieving:
                # print("got more")
                data += message
                # print(data)
            if "[END]" in message:
                # data += message
                # print("found the end")
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
        # if the command has #iperf, only broadcast to the specific number following after #iperf
        try:
            if "iperf" in command:
                # desired_target = command.split("iperf")[1]
                desired_target  = command.replace("iperf", "")
                print("desired_target_id:", desired_target , "client add", client_address[0][-1])
                if desired_target.strip() in client_address[0][-1].strip():
                    print("correct address")
                    connection.sendall(f"iperf\n".encode())
                    continue
            else:
                print(f"Client address: {client_address}")
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
