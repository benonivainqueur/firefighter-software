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
import asyncio

# import __init__
import sys
import random
sys.path.append( sys.path[0] + "/..")
import tapstrap.realtime_inference 
import schedule 
import time 


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
        self.ip = None
        self.server_ip = "192.168.8.243"
        self.server_port = 5555
        self.connected = False
        self.id = id
        self.neighbors = []
        self.last_updated = time.time()
        self.counter = 0
        self.tapstrap_battery = "100"
        self.tapstrap_id = 0
        self.bt_id = "0"
        self.tapstrap_connected = False
        self.gesture = "None"
        self.connection_tree = {}
        self.bit_rate = "None"
        self.tapstrap_shared_queue = tapstrap.realtime_inference.shared_queue
        self.disconnect_time = 0

    def update_location(self, new_location=None):
        """
        Updates the location of the firefighter.

        Parameters:
        - new_location (str): The new location of the firefighter.
        """
        self.location = new_location
        self.update_time()

    def update_neighbors(self):
        """
        Updates the list of neighboring firefighters.

        Parameters:
        - new_neighbors (list): The new list of neighboring firefighters.
        """
        # self.neighbors = new_neighbors

        # run wifi scan, get the list of wifi networks and their signal strengths
        # self.neighbors = wifi.scan()
        self.neighbors = ["John", "Sarah", "Michael"]
        self.update_time()

    def update_time(self):
        """
        Updates this Firefighters last updated timestamp.
        """
        self.last_updated = time.time()
    
    def send_data(self):
        """
        Converts the Firefighter object to a JSON string.

        Returns:
        - str: The JSON representation of the object.
        """
        if not f1.tapstrap_shared_queue.empty():
            gesture = f1.tapstrap_shared_queue.get(block=False)
            f1.gesture = gesture
            print(f"Gesture: {gesture}")
        else:
            print("gesture queue is empty.")
        
        # delete client object
        # d = {k: v for k, v in d.items() if k != "client"}
        d = self.__dict__.copy()
        d.pop("tapstrap_shared_queue")
        d.pop("client")
        # d["tapstrap_shared_queue"] = list(self.__dict__["tapstrap_shared_queue"])

        d = json.dumps(d, skipkeys=True, default=str)
        self.client.sendall(d.encode())

       
        # if f1.connected:
            # f1.send_data()
            
        # send data to the server
        # return d

    def update_ip(self):
        """
        Retrieves the IP address of the firefighter's device.

        Returns:
        - str: The IP address.
        """
        print("updating ip")
        try:
            ip = subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.split(" ")[0]
            self.ip = ip
        except:
            self.ip = "Error"
    def update_tapstrap_battery(self):
        """
        Updates the TapStrap battery level.
        """
        # get the battery level of the tapstrap
        # use bluetooth to get the battery level
        # self.tapstrap_battery = bluetooth.get_battery_level()
        self.tapstrap_battery = "100"
        self.update_time()
    
    

    def run_tapstrap_subprocess(self):
            """
            Runs the TapStrap subprocess.

            This method starts the TapStrap subprocess and continuously retrieves
            gesture predictions from the shared queue. It assigns the latest gesture
            to the `self.gesture` attribute and prints the value of the gesture.

            Note: This method requires the `asyncio` library and a running event loop.
            """
            
            # last in first out queue to ensure we always get the most recent prediction
            loop = asyncio.get_event_loop() # we need this loop to run the tapstrap inference since it uses asyncio
            threading.Thread(target=tapstrap.realtime_inference.main, args=(True,loop,)).start()
            self.tapstrap_connected = True
            # threading.Thread(target=tapstrap.realtime_inference.main, args=(True,loop,)).start()

            # tapstrap.realtime_inference.main(False)
            # while not shared_queue.empty():
            # while True:
            #     gesture = shared_queue.get()
            #     self.gesture = gesture
                # print("queue value", gesture)

    def to_json(self):
        """
        Converts the Firefighter object to a JSON string.

        Returns:
        - str: The JSON representation of the object.
        """
        return json.dumps(self.__dict__)

    def update_wifi_strength(self):
        """
        Updates this firefighters WiFi strength.

        Returns:
        - str: The WiFi strength.
        """
        try :
            command_output = subprocess.run(['iw', 'dev', 'wlan0', 'link'], capture_output=True, text=True)
            signal_level = [line for line in command_output.stdout.split('\t') if len(line) > 0]
            signal_level = [line.replace("\n", "") for line in signal_level]
            print(signal_level) 
            self.wifi_strength = signal_level[5]
            self.wifi_network_name = signal_level[1]
            self.bit_rate = signal_level[6]
        except Exception as e:
            self.wifi_strength = "Error"
            self.wifi_network_name = "Error"
            self.bit_rate = "Error"
        # return signal_level[5]
        self.update_time()

    def route_wifi_data(self):
        """
        Routes WiFi data to the server or the nearest firefighter.
        """
        print("routing wifi data")
        pass
    
    def route_bluetooth_data(self):
        """
        Routes Bluetooth data to the server or the nearest firefighter.
        """
        print("routing bluetooth data")
        return None
        pass

    def update_connection_tree(self):
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
        return f"{self.name} is at {self.location}, Connected to {self.server_ip}:{self.server_port}"
    
    ############ CLIENT ################

    def run_client(self, server_ip, server_port):
        """
        Connects to the server using the provided IP address and port number.
        
        Args:
            server_ip (str): The IP address of the server.
            server_port (int): The port number of the server.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, int(self.server_port)))
        self.connected = True
        # self.data = None

    # def get_client_data(self):
    #     self.data = self.client.recv(1024).decode()
    #     return self.data
    
    # def send_data(self, data):
    #     self.client.sendall(data.encode())

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
    counter = 0
    while not f1.connected:
        try:
            f1.run_client(f1.server_ip,f1.server_port)
        except Exception as e:
            print("attempt {} connecting to server, trying again in 3 seconds".format(counter))
            time.sleep(1)
        counter +=1  
        if counter > 5:
            print("Failed to connect to server after 5 attempts, exiting.")
            break

    counter = 0
    while not f1.tapstrap_connected:
        try: 
            f1.run_tapstrap_subprocess()
        except Exception as e:
            print("failed to run tapstrap subprocess attempt {}, trying again in 3 seconds".format(counter))
            time.sleep(1)
        counter += 1
        if counter > 5:
            print("Failed to connect to tapstrap after {} attempts, exiting.".format(counter))

    # s = sched.scheduler()
    
    # s.enter(5,1, f1.get_wifi_strength)
    # indicate what events to schedule, the time between each event and the function to call
    events = [
        (2, 1, f1.update_wifi_strength),
        (2,1, f1.update_tapstrap_battery),
        (2,1, f1.update_connection_tree),
        (2,1, f1.update_neighbors),
        (2,1, f1.update_ip),
        (2,1,  f1.update_location),
        (1,1, f1.send_data), # send data to the server
        (1,1, f1.route_wifi_data),
        (2,1, f1.route_bluetooth_data),
        # (10,1, f1.update_time),
        ]
    # schedule the events
    for e in events:
        schedule.every(e[0]).seconds.do(e[2])
    
    while True:
        schedule.run_pending()
        time.sleep(1)

    # while True:
    # s.run(blocking=False)
    # time.sleep(100)
    # time.sleep(1)
    # s.run()
# Run job every 3 second/minute/hour/day/week,
        
        
# Starting 3 second/minute/hour/day/week from now
# schedule.every(3).seconds.do(job)
# schedule.every(3).minutes.do(job)
# schedule.every(3).hours.do(job)
# schedule.every(3).days.do(job)
# schedule.every(3).weeks.do(job)

# # Run job every minute at the 23rd second
# schedule.every().minute.at(":23").do(job)

# # Run job every hour at the 42nd minute
# schedule.every().hour.at(":42").do(job)

# # Run jobs every 5th hour, 20 minutes and 30 seconds in.
# # If current time is 02:00, first execution is at 06:20:30
# schedule.every(5).hours.at("20:30").do(job)

# # Run job every day at specific HH:MM and next HH:MM:SS
# schedule.every().day.at("10:30").do(job)
# schedule.every().day.at("10:30:42").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)

# # Run job on a specific day of the week
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)





    # while True:
    #     # wait 1 second
    #     time.sleep(1)
        # while True:
        # dont halt the program if theres nothing in the queue, just print that theres nothing
        # check if not empty
      
        # f1.last_updated = time.time()
        # f1.get_wifi_strength()
        # client.send_data(f1.to_json())  
        # time.sleep(.5)
        # f2.last_updated = time.time()
        # f2.neighbors = 1
        # client.send_data(f2.to_json())
        
    #     print(f"sent {len(f1.to_json())} bytes to the server")
    # run the tapstrap subprocess in a thread
    # import threading
    # t1 = threading.Thread(target=run_tapstrap_subprocess, args=(output_queue,))
    # run_tapstrap_subprocess(output_queue=output_queue)
    # t1.start()
    # print("Subprocess exited with return code:")
    # Print live output from the queue
    # while not output_queue.empty():
    #     print(output_queue.get())
    # f1.tapstrap_inference()
        
        # print("sent data too server")      