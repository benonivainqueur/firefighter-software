import tkinter as tk
from tkinter import ttk
import socket
import json
import threading
import time
import matplotlib.pyplot as plt

from tkinter import filedialog
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import __init__
# print(sys.path)import sys
# sys.path.append( sys.path[0] + "/..")

from tapstrap.tools import connect_to_tapstrap

demo_firefighter_data = [
    {
        "name": "John",
        "location": "Building A, Floor 2",
        "gesture": "None",
        "id": 0,
        "wifi_strength": "Excellent",
        "last_updated": "10 Seconds Ago",

    },
    {
        "name": "Sarah",
        "location": "Building A, Floor 2",
        "gesture": "None",
        "id": 1,
        "wifi_strength": "Good",
        "last_updated": "100 seconds ago",
    },
    # {
    #     "name": "Michael",
    #     "location": "Building A, Floor 2",
    #     "gesture": "None",
    #     "id": 2,
    #     "wifi_strength": "Bad",
    #     "last_updated": "300 Seconds Ago",

    # },

    #  {
    #     "name": "Ben",
    #     "location": "Building A, Floor 2",
    #     "gesture": "None",
    #     "id": 3,
    #     "wifi_strength": "Bad",
    #     "last_updated": "300 Seconds Ago",

    # },
    #    {
    #     "name": "uh",
    #     "location": "Building A, Floor 2",
    #     "gesture": "None",
    #     "id": 4,
    #     "wifi_strength": "Bad",
    #     "last_updated": "300 Seconds Ago",

    # }

]
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