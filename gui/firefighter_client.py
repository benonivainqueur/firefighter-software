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
# import __init__
import sys
import random
sys.path.append( sys.path[0] + "/..")


def get_demo_firefighter_data():
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
    """
    Represents a firefighter with various attributes and functionalities.

    Attributes:
    - id (int): The ID of the firefighter.
    - name (str): The name of the firefighter.
    - location (str): The current location of the firefighter.
    - wifi_strength (str): The strength of the WiFi signal.
    - wifi_network_name (str): The name of the WiFi network.
    - ip (str): The IP address of the firefighter's device.
    - server_ip (str): The IP address of the server.
    - server_port (int): The port number of the server.
    - neighbors (list): The list of neighboring firefighters.
    - last_updated (float): The timestamp of the last update.
    - counter (int): A counter for internal use.
    - tapstrap_battery (str): The battery level of the TapStrap device.
    - tapstrap_id (int): The ID of the TapStrap device.
    - bt_id (str): The ID of the Bluetooth device.
    - tapstrap_connected (str): Indicates if the TapStrap device is connected.
    - gesture (str): The current gesture detected by the TapStrap device.
    - connection_tree (dict): The connection tree of firefighters.
    - bit_rate (str): The bit rate of the WiFi connection.
    """

    def __init__(self, id, name, location):
        """
        Initializes a new instance of the Firefighter class.

        Parameters:
        - id (int): The ID of the firefighter.
        - name (str): The name of the firefighter.
        - location (str): The current location of the firefighter.
        """
        self.name = name
        self.location = location
        self.wifi_strength = "Excellent"
        self.wifi_network_name = "FirefighterNet"
# self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = self.get_ip()
        self.server_ip = "192.168.0.30"
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
        self.bit_rate = "None"

    def update_location(self, new_location):
        """
        Updates the location of the firefighter.

        Parameters:
        - new_location (str): The new location of the firefighter.
        """
        self.location = new_location
        self.update_time()

    def update_wifi_strength(self, new_strength):
        """
        Updates the WiFi strength of the firefighter.

        Parameters:
        - new_strength (str): The new WiFi strength.
        """
        self.wifi_strength = new_strength
        self.update_time()

    def update_neighbors(self, new_neighbors):
        """
        Updates the list of neighboring firefighters.

        Parameters:
        - new_neighbors (list): The new list of neighboring firefighters.
        """
        self.neighbors = new_neighbors
        self.update_time()

    def update_time(self):
        """
        Updates the last updated timestamp.
        """
        self.last_updated = time.time()

    def send_data(self, data):
        """
        Sends data to the server.

        Parameters:
        - data: The data to be sent.
        """
        # send data to the server
        pass

    def get_ip(self):
        """
        Retrieves the IP address of the firefighter's device.

        Returns:
        - str: The IP address.
        """
        try:
            ip = subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.split(" ")[0]
            return ip
        except:
            self.ip = "Error"

    def run_tapstrap_subprocess():
        """
        Runs the TapStrap subprocess.
        """
        import tapstrap.realtime_inference 
        output_queue = queue.Queue()
        shared_queue = tapstrap.realtime_inference.shared_queue
        threading.Thread(target=tapstrap.realtime_inference.main, args=(False,)).start()

        while not shared_queue.empty():
            a = shared_queue.get()
            
            print("queue value", a)

    def to_json(self):
        """
        Converts the Firefighter object to a JSON string.

        Returns:
        - str: The JSON representation of the object.
        """
        return json.dumps(self.__dict__)

    def get_wifi_strength(self):
        """
        Retrieves the WiFi strength.

        Returns:
        - str: The WiFi strength.
        """
   
        command_output = subprocess.run(['iw', 'dev', 'wlan0', 'link'], capture_output=True, text=True)
        signal_level = [line for line in command_output.stdout.split('\t') if len(line) > 0]
        signal_level = [line.replace("\n", "") for line in signal_level]
        print(signal_level) 
        self.wifi_strength = signal_level[5]
        self.wifi_network_name = signal_level[1]
        self.bit_rate = signal_level[6]
        return signal_level[5]

    def route_wifi_data(self):
        """
        Routes WiFi data to the server or the nearest firefighter.
        """
        pass
    
    def route_bluetooth_data(self):
        """
        Routes Bluetooth data to the server or the nearest firefighter.
        """
        pass

    def build_connection_tree(self):
        """
        Builds a connection tree.
        """
        pass

    def __str__(self):
        """
        Returns a string representation of the firefighter.

        Returns:
        - str: The string representation.
        """
        return f"{self.name} is at {self.location}"
    
    ############ CLIENT ################

    def client(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, int(self.server_port)))
        self.data = None

    def get_data(self):
        self.data = self.client.recv(1024).decode()
        return self.data

    def __str__(self):
        return f"Connected to {self.server_ip}:{self.server_port}"
    
    def send_data(self, data):
        self.client.sendall(data.encode())




# main method 


# Example usage:
# if __name__ == "__main__":


        

# class FirefighterClient:

    
#     firefighter1 = Firefighter(1,"John", "Building A, Floor 2" )
#     firefighter2 = Firefighter(2,"Sarah", "Building A, Floor 2" )
#     firefighter3 = Firefighter(3,"Michael", "Building A, Floor 2" )



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
    f1 = Firefighter(1, "John", "Building A, Floor 2")
    # f2 = Firefighter(2, "Sarah", "Building B, Floor 32")
    f1.client("192.168.0.30","5555")
    # while True:
    #     # wait 1 second
    #     time.sleep(.5)
    #     f1.last_updated = time.time()
    #     f1.get_wifi_strength()
    #     client.send_data(f1.to_json())  
    #     time.sleep(.5)
    #     f2.last_updated = time.time()
    #     f2.neighbors = 1
    #     client.send_data(f2.to_json())
        
    #     print(f"sent {len(f1.to_json())} bytes to the server")
    output_queue = queue.Queue()
    # run the tapstrap subprocess in a thread
    # import threading
    # t1 = threading.Thread(target=run_tapstrap_subprocess, args=(output_queue,))
    # run_tapstrap_subprocess(output_queue=output_queue)
    # t1.start()
    # print("Subprocess exited with return code:")
    # Print live output from the queue
    f1.run_tapstrap_subprocess(output_queue=output_queue)
    while not output_queue.empty():
        print(output_queue.get())
    # f1.tapstrap_inference()
        
        # print("sent data too server")      