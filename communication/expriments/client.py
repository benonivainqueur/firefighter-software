import subprocess
import socket
import ntplib
import json
from time import ctime

# Function to run iperf3 test and collect output
def run_iperf_test():
    iperf_output = subprocess.run(['iperf3', '-c', 'server_ip', '--json'], capture_output=True)
    return iperf_output.stdout.decode("utf-8")

# Function to send iperf3 and ping data to server
def send_data_to_server(server_ip, server_port, iperf_data, ping_data):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))

        # Combine iperf3 and ping data into a single JSON object
        combined_data = {"iperf": json.loads(iperf_data), "ping": ping_data}
        
        # Convert the combined data to JSON string
        json_data = json.dumps(combined_data)

        # Send the combined data to the server
        client_socket.sendall(json_data.encode("utf-8"))
        print("Data sent to server successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the socket
        client_socket.close()

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

# Function to ping detected neighbors
def ping_neighbors(detected_neighbors):
    ping_results = {}
    try:
        for neighbor in detected_neighbors:
            # Ping neighbor and capture output
            ping_output = subprocess.run(['ping', '-c', '4', neighbor], capture_output=True, text=True)

            # Parse ping output for statistics
            ping_result = parse_ping_output(ping_output.stdout)

            # Store ping statistics in dictionary
            ping_results[neighbor] = ping_result

    except Exception as e:
        print(f"Error pinging neighbors: {e}")

    return ping_results

# Function to parse ping output and extract statistics
def parse_ping_output(ping_output):
    # Parse ping output for statistics
    # Example output: "4 packets transmitted, 4 received, 0% packet loss, time 3003ms"
    lines = ping_output.split('\n')
    stats_line = lines[-2]  # Second-to-last line contains the statistics

    # Extract ping statistics
    stats_parts = stats_line.split(', ')
    packet_transmitted = int(stats_parts[0].split()[0])
    packet_received = int(stats_parts[1].split()[0])
    packet_loss = float(stats_parts[2].split()[0][:-1])  # Remove '%' character
    round_trip_min = int(stats_parts[3].split()[1])
    round_trip_avg = int(stats_parts[4].split()[1])
    round_trip_max = int(stats_parts[5].split()[1])
    round_trip_mdev = int(stats_parts[6].split()[1])

    # Construct dictionary with ping statistics
    ping_stats = {
        "packet_transmitted": packet_transmitted,
        "packet_received": packet_received,
        "packet_loss": packet_loss,
        "round_trip_min": round_trip_min,
        "round_trip_avg": round_trip_avg,
        "round_trip_max": round_trip_max,
        "round_trip_mdev": round_trip_mdev
    }

    return ping_stats

def detect_neighbors_batman():
    try:
        # Run the command to get BATMAN-Adv neighbor information
        batman_output = subprocess.run(['batctl', 'o'], capture_output=True, text=True)

        # Parse BATMAN-Adv output to extract neighbor IP addresses
        neighbor_ips = []
        lines = batman_output.stdout.split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) > 2 and parts[1] == 'reachable':
                neighbor_ips.append(parts[0])

        return neighbor_ips

    except Exception as e:
        print(f"Error detecting neighbors using BATMAN-Adv: {e}")
        return []

def detect_neighbors_olsr():
    try:
        # Run the command to get OLSR neighbor information
        olsr_output = subprocess.run(['olsrd', '-f', '/etc/olsrd/olsrd.conf', '-h'], capture_output=True, text=True)

        # Parse OLSR output to extract neighbor IP addresses
        neighbor_ips = []
        lines = olsr_output.stdout.split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) > 2 and parts[1] == 'NEIGH':
                neighbor_ips.append(parts[2])

        return neighbor_ips

    except Exception as e:
        print(f"Error detecting neighbors using OLSR: {e}")
        return []

# # Example usage:
# olsr_neighbors = detect_neighbors_olsr()
# print("OLSR Neighbors:", olsr_neighbors)
    
def main():
    # Define server IP address and port
    server_ip = '172.27.0.0'  # Replace 'server_ip' with the actual server's IP address
    server_port = 12345  # Server's port number
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the server IP address and port
    server_socket.bind((server_ip, server_port))
    while True:
        server_socket.listen(1)
        print("Server is listening for incoming connections...")
        command = server_socket.recv(4096).decode("utf-8")
        print("Command received:", command)
            # Execute the command
        execute_command(command)
        # Run iperf3 test and collect output
        iperf_data = run_iperf_test()

        # Synchronize clocks after each test
        synchronize_clocks()

        # Ping detected neighbors
        detected_neighbors = detect_neighbors_batman()
        print("Detected Neighbors:", detected_neighbors)
        # detected_neighbors = ['neighbor1_ip', 'neighbor2_ip', 'neighbor3_ip']  # List of detected neighbor IP addresses
        ping_data = ping_neighbors(detected_neighbors)

        # Send iperf3 and ping data to server
        send_data_to_server(server_ip, server_port, iperf_data, ping_data)

if __name__ == "__main__":
    main()


import socket
import subprocess

# Function to execute command received from server
def execute_command(command):
    try:
        # Execute the command using subprocess
        subprocess.run(command, shell=True)

    except Exception as e:
        print(f"Error executing command: {e}")

# def main():
    # Define server IP address and port
#     server_ip = 'server_ip'  # Replace 'server_ip' with the actual server's IP address
#     server_port = 12345  # Server's port number

#     # Create a socket object

#     while True:
#         # Accept incoming connection
#         client_socket, client_address = server_socket.accept()
#         print(f"Connection established with {client_address}")

#         try:

#             # Receive command from the server
#             command = client_socket.recv(4096).decode("utf-8")

#         except Exception as e:
#             print(f"Error: {e}")

#         finally:
#             # Close the client socket
#             client_socket.close()

#     # Close the server socket
#     server_socket.close()

# if __name__ == "__main__":
#     main()
