import subprocess
import socket
import ntplib
import json
import time
from time import ctime
import os 

import socket
import subprocess
import subprocess
import socket
import json

# get $PI_ID
pi_id = os.environ.get("PI_ID")
# Function to run iperf3 test and collect output

def execute_command(command):
    try:
        # Execute the command using subprocess
        # remove \n from the command
        command = command.strip()
        print("executing command:", command, "on pi#", pi_id)
        # if command == "batman":
        # output = subprocess.run(['bash', 'interface.sh', command ], capture_output=True)
        # capture all of the future outputs as well
        # wait for the process to finish
        output = ''
        if "ping" in command:
            output = subprocess.run(['bash', 'interface.sh',command ], capture_output=True)
            output = output.stdout.decode("utf-8") + output.stderr.decode("utf-8")
            # output = output.stderr.decode("utf-8")
        elif "close" in command:
            # end the python script
            print("exiting program")
            exit()
        else :
        # output = subprocess.run(['bash', 'interface.sh', command ], capture_output=True)
            output = subprocess.run(['bash', 'interface.sh', command ], capture_output=True)
            output = output.stdout.decode("utf-8")
        

        # get raw string from output
        print("OUTPUT:", output)
        # elif command == "olsr":
            # output = subprocess.run(['./start_olsr.sh'], capture_output=True)
        # elif command == "iperf":
            # output = subprocess.run(['./run_iperf.sh'], capture_output=True)

        # subprocess.run(command, shell=True)
        # print("output:", output)
        return output

    except Exception as e:
        print(f"Error executing command: {e}")

# Function to send data to server
def send_data_to_server(server_socket, data, command):
    try:
        print("in send_data_to_server, the command recieved was:", command)
        if "iperf" in command:
            # Convert data to JSON string with no spaces or newlines
            json_data = json.dumps(data, indent=None)
            # remove all spaces and newlines from the json_data
            # print("Data to send:", json_data)

            # Send the data to the server
            #send "[START]" to indicate the start of the data
            server_socket.sendall("[START]".encode())
            # clean the json data
            json_data = json_data.replace("\\n", "")
            json_data = json_data.replace("\\t", "")
            json_data = json_data.replace("\\", "")

            server_socket.sendall(json_data.encode())
            # send "[END]" to indicate the end of the data
            server_socket.sendall("[END]".encode())
            # print("Data sent to server successfully.")
            print("iperf sent to server:", json_data)
        if "ping" in command :
            server_socket.sendall("[START]".encode())
            server_socket.sendall(data.encode())
            # send "[END]" to indicate the end of the data
            server_socket.sendall("[END]".encode())
            # print("Data sent to server successfully.")
            print("ping data sent to server:", data)

    except Exception as e:
        print(f"Error sending data to server: {e}")

def main():
    # Define server IP address and port
    server_ip = '172.27.0.0'  # Replace 'server_ip' with the actual server's IP address
    server_port = 12345  # Server's port number

    while True:
        try:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            client_socket.connect((server_ip, server_port))
            print("Connected to server.")

            while True:
                # Receive command from server
                
                command = client_socket.recv(4096).decode("utf-8")
                if command:
                    print("Command received:", command)

                # Execute the command
                    data = execute_command(command)

                # Send iperf3 data to server
                    send_data_to_server(client_socket, data, command)

        except Exception as e:
            print(f"Error: {e}")
            print("Reconnecting to the server in 1 second...")
            time.sleep(1)

        finally:
            # Close the socket
            if client_socket:
                client_socket.close()

if __name__ == "__main__":
    main()
