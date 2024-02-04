import time
import socket
import json
import os 
# import system 
# use the system module to get the computer name
# import bluetooth and wifi modules
# import bluetooth
# import wifi
# from realtime_inference import 
import subprocess
import queue
import threading


class Firefighter:
    def __init__(self, id,name, location ):
        self.name = name
        self.location = location
        self.wifi_strength = "Excellent"
        self.wifi_network_name = "FirefighterNet"
        self.ip = ''
        self.port = 5555
        self.id = id
        self.neighbors = []
        self.last_updated = time.time()
        self.counter = 0
        self.tapstrap_id = 0
        self.tapstrap_connected = False
        self.connection_tree = {}
        # self.pc_name = os.environ['COMPUTERNAME']   # get the computer name

    def update_location(self, new_location):
        self.location = new_location
        self.update_time()

    
    def update_wifi_strength(self, new_strength):
        self.wifi_strength = new_strength
        self.update_time()

    def update_neighbors(self, new_neighbors):
        self.neighbors = new_neighbors
        # will use the wifi module to list out the neighbors
        self.update_time()

    def update_time(self):
        self.last_updated = time.time()
        
    def send_data(self, data):
        # send data to the server
        #
        pass

    #### TAPSTRAP FUNCTIONS ####

    def connect_to_tapstrap(self, tapstrap_id):
        # connect to the tapstrap
        self.tapstrap_id = tapstrap_id
        self.tapstrap_connected = True
        pass
    
    def gesture_recognition(self):
        # perform gesture recognition
        pass

    def to_json(self):
        return json.dumps(self.__dict__)

    ### WIFI/ BLUETOOTH FUNCTIONALITY

    def route_wifi_data(self):
        # route wifi data to the server, or the nearest firefighter
        pass
    
    def route_bluetooth_data(self):
        # route bluetooth data to the server, or the nearest firefighter
        pass

    def build_connection_tree(self):
        # build a connection tree
        pass

    def __str__(self):
        return f"{self.name} is at {self.location}"

# main method 
def run_tapstrap_subprocess(file_path="realtime_inference.py", output_queue = None):
    """
    Run a Python file in a subprocess and extract live output into a queue.

    Args:
    - file_path (str): The path to the Python file to run.
    - output_queue (Queue): A queue to store live output from the subprocess.

    Returns:
    - subprocess.CompletedProcess: The completed process object.
    """
    # Function to read output from the subprocess and put it into the queue
    def read_output(process, output_queue):
        print("output: ", process.stdout.readline())
        for line in iter(process.stdout.readline, b''):
            output_queue.put(line.encode().strip())  # Assuming the output is text

    # Run the Python file in a subprocess
    process = subprocess.Popen(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    # Start a thread to read output from the subprocess
    output_thread = threading.Thread(target=read_output, args=(process, output_queue))
    output_thread.start()
    print("output_thread", output_thread)

    # Wait for the subprocess to finish
    process.wait()

    # Wait for the output thread to finish
    output_thread.join()

    return process

# Example usage:
# if __name__ == "__main__":


        

# class FirefighterClient:
#     def __init__(self, server_ip, server_port):
#         self.server_ip = server_ip
#         self.server_port = server_port
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client.connect((self.server_ip, self.server_port))
#         self.data = None

#     def get_data(self):
#         self.data = self.client.recv(1024).decode()
#         return self.data

#     def to_json(self):
#         return json.dumps(self.__dict__)

#     def __str__(self):
#         return f"Connected to {self.server_ip}:{self.server_port}"
    

if __name__ == "__main__":
    # connect to the server
    # connect to tap strap 
    # run the realtime_inference.py file 
    output_queue = queue.Queue()
    process = run_tapstrap_subprocess("../tapstrap/realtime_inference.py", output_queue)
    print("Subprocess exited with return code:", process.returncode)

    # Print live output from the queue
    while not output_queue.empty():
        print(output_queue.get())

        