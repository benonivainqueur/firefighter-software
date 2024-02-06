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
# import library to get the current ip add
import socket
import os


def get_demo_firefighter_data():
        import random
        # Create a copy of the demo data
        # print("Getting demo firefighter data")
        demo_data = demo_firefighter_data.copy()
        for firefighter in demo_data:
            # update each time to a random value
            # firefighter["last_updated"] = str(time.time()) # random number between 0 and 100
            firefighter["last_updated"] = random.randint(0, 100)
            # randomize the wifi strength
            firefighter["wifi_strength"] = random.choice(["Excellent", "Good", "Fair", "Poor"])
            # randomize the gesture
            firefighter["gesture"] = random.choice(["0", "1", "2", "3","4"])
            firefighter["ip"] = "100"
            #   ("IP", view_data["ip"]),
            # ("Bluetooth ID", view_data["bt_id"]),
            # ("Tapstrap Connected", view_data["tapstrap_connected"]),
            # ("TapStrap Battery Percent", view_data["tapstrap_battery"]),
            # ("Location", view_data["location_var"]),
            # ("Gesture", view_data["gesture_var"]),
            # ("Wifi Strength", view_data["wifi_strength_var"]),
            # ("Last Updated", view_data["last_updated_var"]),
            firefighter["tapstrap_connected"] = random.choice(["True", "False", "other"])
            firefighter["tapstrap_battery"] = random.randint(0, 100)
            firefighter["bt_id"] = random.choice(["0", "1", "2", "3","4"])
            firefighter["tapstrap_id"] = random.choice(["0", "1", "2", "3","4"])
        
        return demo_data

class Firefighter:
    def __init__(self, id,name, location ):
        self.name = name
        self.location = location
        self.wifi_strength = "Excellent"
        self.wifi_network_name = "FirefighterNet"
        self.ip = socket.gethostbyname(socket.gethostname())
        # self.server_ip = "127.0.0.1"
        self.server_ip =  "192.168.0.30"

        self.server_port = 5555
        self.id = id
        self.neighbors = []
        self.last_updated = time.time()
        self.counter = 0
        self.tapstrap_battery = "100"
        self.tapstrap_id = 0
        self.bt_id = "0"
        self.tapstrap_connected = "False"
        self.gesture = "None"
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

    def get_wifi_strength(self):
        # get the wifi strength
        import subprocess

        # Run the command to get the WiFi signal strength
        # command_output = subprocess.run(['iwconfig', 'wlan0'], capture_output=True, text=True)
        command_output = subprocess.run(['iw', 'dev', 'wlan0', 'link'], capture_output=True, text=True)

        "iw dev wlan0 link"
        # Extract the signal level from the command output
        signal_level = [line for line in command_output.stdout.split('\n') if len(line) > 0]

        # Print the signal level
        print(signal_level) 
        return signal_level[6]
        pass

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


        

class FirefighterClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, int(self.server_port)))
        self.data = None

    def get_data(self):
        self.data = self.client.recv(1024).decode()
        return self.data

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return f"Connected to {self.server_ip}:{self.server_port}"
    
    def send_data(self, data):
        self.client.sendall(data.encode())
    
    firefighter1 = Firefighter(1,"John", "Building A, Floor 2" )
    firefighter2 = Firefighter(2,"Sarah", "Building A, Floor 2" )
    firefighter3 = Firefighter(3,"Michael", "Building A, Floor 2" )
if __name__ == "__main__":
    # connect to the server
    # connect to tap strap 
    # run the realtime_inference.py file 
    # output_queue = queue.Queue()
    # process = run_tapstrap_subprocess("../tapstrap/realtime_inference.py", output_queue)
    # print("Subprocess exited with return code:", process.returncode)

    # # Print live output from the queue
    # while not output_queue.empty():
    #     print(output_queue.get())

    # # Create a firefighter client
    client = FirefighterClient("192.168.0.30", "5555")  
    f1 = Firefighter(1, "John", "Building A, Floor 2")
    f2 = Firefighter(2, "Sarah", "Building B, Floor 32")
    while True:
        # wait 1 second
        time.sleep(.5)
        f1.last_updated = time.time()
        f1.wifi_strength = f1.get_wifi_strength()
        client.send_data(f1.to_json())  
        time.sleep(.5)
        f2.last_updated = time.time()
        f2.neighbors = 1
        client.send_data(f2.to_json())
        
        print(f"sent {len(f1.to_json())} bytes to the server")
        
        # print("sent data too server")      