import socket
import subprocess
import threading

# Global dictionary to store client connections and their addresses
client_connections = {}

def handle_client(connection, client_address):
    try:
        print("Connection established with", client_address)

        # Add client connection to the global dictionary
        client_connections[connection] = client_address
        data = ""
        recieving = False
        while True:
            # Wait for incoming messages from the client
            message = connection.recv(1024).decode()
            if not message:
                break

            print(f"Received message from {client_address}: {message}")
            if message == "disconnecting":
                break
            if "[START]" in message:
                # get pi id from the message
                # we need to start receiving the batman data until we reach the end 
                recieving = True
                data += message
            if recieving:
                data += message
                if "[END]" in message:
                    recieving = False
                    print("final data recieved:", data)
                    data = ""

    except Exception as e:
        print(f"Error handling client connection: {e}")

    finally:
        # Clean up the connection and remove it from the dictionary
        connection.close()
        del client_connections[connection]

def run_iperf_server():
    # Start the iperf3 server
    iperf_server = subprocess.Popen(["./iperf_server.sh"])
    print("iperf3 server started")

def broadcast_command(command):
    # Send the command to all connected clients
    for connection, client_address in client_connections.items():
        try:
            connection.sendall(f"{command}\n".encode())
        except Exception as e:
            print(f"Error sending command to {client_address}: {e}")

command_list = [("batman", "./start_batman.sh"), ("iperf", "iperf3 -c server_ip -t 10")]

def input_thread():
    # Read command from server console and broadcast it to all clients
    while True:
        command = input("Enter command to broadcast: ")
        # switch statement to execute the command
     
        broadcast_command(command)

def server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    # server_ip = '172.27.0.0'  # Listen on all available interfaces
    server_address = ('172.27.0.0', 12345)
    # server_address = ('192.168.0.30', 12345)  # Update the server IP address
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)

    print("Server is listening for incoming connections...")

    try:
        # Start the input thread
        input_thread_handle = threading.Thread(target=input_thread)
        input_thread_handle.start()

        # run iperf3 server in another thread
        iperf_server_thread = threading.Thread(target=run_iperf_server)
        iperf_server_thread.start()

        while True:
            # Wait for a connection
            print("Waiting for a connection...")
            connection, client_address = server_socket.accept()

            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
            client_thread.start()

    except Exception as e:
        print(f"Error in server: {e}")

    finally:
        # Close the server socket
        print("Closing server socket...")
        server_socket.close()

if __name__ == "__main__":
    server()
