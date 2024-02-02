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
    {
        "name": "Michael",
        "location": "Building A, Floor 2",
        "gesture": "None",
        "id": 2,
        "wifi_strength": "Bad",
        "last_updated": "300 Seconds Ago",

    }

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
            firefighter["gesture"] = random.choice(["None", "Gesture 1", "Gesture 2", "Gesture 3"])
        
        return demo_data