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
def run_iperf_test():
    iperf_output = subprocess.run(['iperf3', '-c', 'server_ip', '--json'], capture_output=True)
    return iperf_output.stdout.decode("utf-8")
# Function to execute command received from server

def execute_command(command):
    try:
        # Execute the command using subprocess
        # remove \n from the command
        command = command.strip()
        print("executing command:", command, "on pi#", pi_id)
        output =  ''
        # if command == "batman":
        output = subprocess.run(['bash', 'interface.sh', command ], capture_output=True)
        # get raw string from output
        output = output.stdout.decode("utf-8")
        # elif command == "olsr":
            # output = subprocess.run(['./start_olsr.sh'], capture_output=True)
        # elif command == "iperf":
            # output = subprocess.run(['./run_iperf.sh'], capture_output=True)

        # subprocess.run(command, shell=True)
        # print("output:", output)
        return output

    except Exception as e:
        print(f"Error executing command: {e}")

# Function to send iperf3 and ping data to server
# Function to synchronize clocks using NTP
def synchronize_clocks():
    # Get NTP server address
    ntp_server = 'pool.ntp.org'

    # Create NTP client object
    client = ntplib.NTPClient()

    try:
        # Query NTP server for current time
        response = client.request(ntp_server)

        # Synchronize local clock with NTP server time
        local_time = ctime(response.tx_time)
        subprocess.run(['sudo', 'date', '-s', local_time])
        print(f"Local clock synchronized with NTP server time: {local_time}")

    except Exception as e:
        print(f"Error synchronizing clock: {e}")

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
            print("Data sent to server:", json_data)
        if "ping" in command :
            # Convert data to JSON string with no spaces or newlines
            # json_data = json.dumps(data, indent=None)
            # remove all spaces and newlines from the json_data
            # print("Data to send:", json_data)

            # Send the data to the server
            #send "[START]" to indicate the start of the data
            server_socket.sendall("[START]".encode())
            # clean the json data
            # json_data = json_data.replace("\\n", "")
            # json_data = json_data.replace("\\t", "")
            # json_data = json_data.replace("\\", "")

            server_socket.sendall(data.encode())
            # send "[END]" to indicate the end of the data
            server_socket.sendall("[END]".encode())
            # print("Data sent to server successfully.")
            print("Data sent to server:", json_data)

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
                print("Waiting for command...")
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
