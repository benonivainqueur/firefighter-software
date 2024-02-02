import time
import socket
import json

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

        self.connected_to_tapstrap = False

        self.connection_tree = {}

    def update_location(self, new_location):
        self.location = new_location
        self.last_updated = time.time()
    
    def update_wifi_strength(self, new_strength):
        self.wifi_strength = new_strength
        self.last_updated = time.time()

    def update_neighbors(self, new_neighbors):
        self.neighbors = new_neighbors
        # will use the wifi module to list out the neighbors

        self.last_updated = time.time()
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
        self.connected_to_tapstrap = True
        pass

    def gesture_recognition(self):
        # perform gesture recognition
        pass

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