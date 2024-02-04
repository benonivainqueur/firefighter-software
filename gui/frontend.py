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
from tools import get_demo_firefighter_data
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

def update_treeview(treeview, text, var):
        new_value = var.get()
        # Find the item in the Treeview that corresponds to the label_text
        for item in treeview.get_children():
            if treeview.item(item, "values")[0] == text:
                # Update the value in the Treeview
                treeview.item(item, values=(text, new_value))
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.label = ttk.Label(root, text="Hello, Tkinter!")
        self.root.title("Firefighter Dashboard")
        self.root.geometry("1600x1400")
        self.firefighter_data = {}  # Dictionary to store actual firefighter data
        self.view_data = {}         # Dictionary to store view representation data
        self.folder_path = ""
        # Make the root window resizable
        # self.root.columnconfigure(0, weight=1)  # Make the column expandable
        # self.root.rowconfigure(0, weight=1)     # Make the row expandable

        # Create the left and right frames
        self.root.resizable(height = None, width = None)
        self.left_frame = tk.PanedWindow(self.root, orient="vertical")
        self.left_frame.pack(side="left", padx=10, pady=10, expand=True)
        # self.left_frame.resizable(height = 100, width = 100)

        self.right_frame = tk.PanedWindow(self.root, orient="horizontal")
        
        # self.right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=False)
        self.right_frame.pack(fill="both", expand=True)
        # create bottom frame
        self.bottom_frame = tk.PanedWindow(self.root, orient="horizontal")
        # make the 
        self.bottom_frame.pack()
        # self.bottom_frame.pack(side="bottom", padx=10, pady=10, fill="both", expand=True)
        
        # Make the right frame resizable
        # self.right_frame.columnconfigure(0, weight=1)  # Make the column expandable
        # self.right_frame.rowconfigure(0, weight=1)     # Make the row expandable
        
        # make the left frame resizeable
        # self.left_frame.columnconfigure(0, weight=1)  # Make the column expandable
        # self.left_frame.rowconfigure(0, weight=1)     # Make the row expandable

        # make the bottom frame resizeable
        # self.bottom_frame.columnconfigure(0, weight=1)  # Make the column expandable
        # self.bottom_frame.rowconfigure(0, weight=1)     # Make the row expandable
        
        # put a divider between the firefighter data and the gesture data
        divider = ttk.Separator(self.bottom_frame, orient="horizontal", style="TSeparator")
        divider.pack(fill="x")
        # 
        # Create tabs in the left frame
        self.left_notebook = ttk.Notebook(self.left_frame)
        self.left_notebook.pack(fill="both", expand=True)

        self.tab_record_gestures_left = ttk.Frame(self.left_notebook)
        self.left_notebook.add(self.tab_record_gestures_left, text="Record Gestures (Left)")

        # Create widgets for Record Gestures tab in the left frame
        self.create_record_gestures_widgets(self.tab_record_gestures_left)

        # Create tabs in the right frame
        self.right_notebook = ttk.Notebook(self.right_frame)
        self.right_notebook.pack(fill="both", expand=True)

        self.tab_record_gestures_right = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.tab_record_gestures_right, text="Record Gestures (Right)")
        
        # Create widget for realtime firefighter data on the right
        self.tab_create_firefighter_data = ttk.Frame(self.right_notebook)
        self.right_notebook.add(self.tab_create_firefighter_data, text="Realtime Firefighter Data")
        self.create_firefighter_data_widgets(self.tab_create_firefighter_data)

        # Create widgets for Record Gestures tab in the right frame
        self.create_record_gestures_widgets(self.tab_record_gestures_right)

        # Labels to display data
        self.strength_label = ttk.Label(root, text="Bluetooth/Wi-Fi Strength:")
        self.strength_label.pack()

        self.names_label = ttk.Label(root, text="Firefighter Names:")
        self.names_label.pack()

        self.locations_label = ttk.Label(root, text="Firefighter Locations:")
        self.locations_label.pack()

        self.time_label = ttk.Label(root, text="Time:")
        self.time_label.pack()

        # Button to refresh data
        self.refresh_button = ttk.Button(root, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.pack()

        # Create the main notebook with tabs
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab_record_gestures = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Realtime Inference")
        self.notebook.add(self.tab2, text="Realtime Firefighter Data")
        self.notebook.add(self.tab_record_gestures, text="Record Gestures")

        # Make the main notebook resizable
        self.tab1.columnconfigure(0, weight=1)
        self.tab1.columnconfigure(1, weight=1)
        self.tab1.rowconfigure(0, weight=1)

        self.create_record_gestures_widgets(self.tab_record_gestures)

        self.create_matplotlib_plot(self.tab1)

        # self.create_firefighter_data_widgets(self.tab2)

        def correctly_resize(event):
            self.canvas_widget.config(width=event.width, height=event.height)
            self.canvas.draw()

            self.tab1.bind("<Configure>", correctly_resize)
            self.canvas_widget.pack(expand=True, fill=tk.BOTH)
        
        self.server_host = "127.0.0.1"
        self.server_port = 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))
        self.refresh_data()


        # l = self.render_firefighter_data()

    # def create_firefighter_data_widgets(self, tab_frame):
        
    #     self.rendred_firefighters  = demo_firefighter_data
    #     for firefighter in self.rendred_firefighters:
    #         # put a divider between the firefighter data
    #         divider = ttk.Separator(tab_frame, orient="horizontal", style="TSeparator")
    #         divider.pack(fill="x")
    #         firefighter["gesture"] = tk.StringVar()
    #         firefighter["gesture"].set("None")
    #         firefighter["frame"] = tk.Frame(tab_frame)
    #         firefighter["frame"].pack()
    #         firefighter["name_label"] = tk.Label(firefighter["frame"], text=firefighter["name"])
    #         firefighter["name_label"].pack()
    #         firefighter["location_label"] = tk.Label(firefighter["frame"], text=firefighter["location"])
    #         firefighter["location_label"].pack()
    #         # firefighter["gesture_label"] = tk.Label(firefighter["frame"], textvariable=firefighter["gesture"])
    #         firefighter["gesture_label"] = tk.Label(firefighter["frame"], textvariable=firefighter["gesture"])

    #         firefighter["gesture_label"].pack()
    #         firefighter["id"] = tk.Label(firefighter["frame"], text=firefighter["id"])
    #         firefighter["id"].pack()
    #         firefighter["wifi_strength_label"] = tk.Label(firefighter["frame"], text="Wifi Strength: Excellent")
    #         firefighter["wifi_strength_label"] = tk.Label(firefighter["frame"], text="Wifi Strength:"+firefighter["wifi_strength"])
    #         firefighter["wifi_strength_label"].pack()
    #         firefighter["last_updated_label"] = tk.Label(firefighter["frame"], text="Last Updated: {} seconds ago".format(firefighter["last_updated"]))

    #         # color code the wifi strength
    #         if "Excellent" in firefighter["wifi_strength"]:
    #             firefighter["wifi_strength_label"].config(fg="green")
    #         elif "Good" in firefighter["wifi_strength"]:
    #             firefighter["wifi_strength_label"].config(fg="blue")
    #         elif "Fair" in firefighter["wifi_strength"]:
    #             firefighter["wifi_strength_label"].config(fg="orange")
    #         elif "Poor" in firefighter["wifi_strength"]:
    #             firefighter["wifi_strength_label"].config(fg="red")
            

    #     self.rendred_firefighters[0]["id"].config(text="699")
    #     self.rendred_firefighters[1]["gesture"].set("69")
    
        # self.firefighter_data = {}  # Dictionary to store actual firefighter data
        # self.view_data = {}         # Dictionary to store view representation data

    def create_firefighter_data_widgets(self, tab_frame):
        demo_firefighter_data = get_demo_firefighter_data()  # Assuming you have a function to get demo firefighter data
        
        for firefighter in demo_firefighter_data:
            firefighter_id = firefighter["id"]
            self.create_firefighter_widget(tab_frame, firefighter_id, firefighter)
            self.update_firefighter_widget(firefighter_id, firefighter)
  

    def create_firefighter_widget(self, tab_frame, firefighter_id, firefighter_data):
        # Create and pack separator
        divider = ttk.Separator(tab_frame, orient="horizontal")
        divider.pack(fill="x")

        # Create frame for firefighter widget
        frame = tk.Frame(tab_frame)
        frame.pack()

        # Store firefighter data in firefighter_data dictionary using firefighter_id as key
        self.firefighter_data[firefighter_id] = firefighter_data

        # Create view representation data and store it using firefighter_id as key
        view_data = {
            "name_var": tk.StringVar(value=firefighter_data["name"]),
            "id": tk.StringVar(frame, value=firefighter_data["id"]),
            "location_var": tk.StringVar(value=firefighter_data["location"]),
            "gesture_var": tk.StringVar(value="None"),
            "wifi_strength_var": tk.StringVar(value="None"),
            "last_updated_var": tk.StringVar(value="None"),
            "frame": frame
        }
        self.view_data[firefighter_id] = view_data

        # Create and pack labels
        labels = [
            ("Name", view_data["name_var"]),
            # ("ID", firefighter_id),
            # ("ID", view_data["id"])
            # ("IP", "123.456.789.0"),
            # ("Bluetooth ID", "1234567890"),
            # ("Tapstrap Connected", "True"),
            # ("TapStrap Battery", "100%"),
            ("Location", view_data["location_var"]),
            ("Gesture", view_data["gesture_var"]),
            ("Wifi Strength", view_data["wifi_strength_var"]),
            ("Last Updated", view_data["last_updated_var"]),
        ]
        # for label_text, label_var in labels:
        #     label = tk.Label(frame, text=label_text + ": ", anchor="e")
        #     # label.pack(side=tk.LEFT, padx=5, pady=5)
        #     label.pack()
        #     # justfiy the text such that everything is evenly spaced 
        #     value_label = tk.Label(frame, textvariable=label_var)
        #     # value_label.pack(side=tk.LEFT, padx=5, pady=5)
        #     value_label

        # for label_text, label_var in labels:
        #     label = tk.Label(frame, text=label_text + ": ", anchor="e")
        #     # label.pack()
        #     value_label = tk.Label(frame, textvariable=label_var)
        #     # value_label.pack()

        # Create and pack treeview widget
        treeview = ttk.Treeview(frame, columns=("name", "value"), show="headings")
        treeview.pack()
        treeview.heading("name", text="firefighter name:")
        treeview.heading("value", text=firefighter_data["name"])
        # Insert firefighter data as rows in the table
        for label_text, label_var in labels:
            treeview.insert("", "end", values=(label_text, label_var.get()))

            # Trace changes in the StringVar and update Treeview
            label_var.trace("w", lambda *args, var=label_var, text=label_text: update_treeview(treeview, text, var))


        # for label_text, label_var in labels:
        #     treeview.insert("", "end", values=(label_text, label_var.get()))
        # for label_text, label_var in labels:
        #     # label_text = tk.Label(frame, text=label_text + ": ", anchor="e")
        #     # label_var = tk.Label(frame, textvariable=label_var)
        #     # treeview.insert("", "end", values=(label_text, label_var))
        #     treeview.insert("", "end", values=(label_text, label_var))
    # Function to update Treeview with new values
  
    def update_firefighter_widget(self, firefighter_id, new_firefighter_data):
        # Update actual firefighter data
        print("firefighter id: ", firefighter_id)
        # for data in self.firefighter_data[firefighter_id]:
        #     view_data = self.view_data[firefighter_id]

            
        # print("data", data)
        self.firefighter_data[firefighter_id].update(new_firefighter_data)

        # Update view representation data
        view_data = self.view_data[firefighter_id]
        
        view_data["gesture_var"].set(new_firefighter_data["gesture"])
        # view_data["wifi_strength_var"].set("Wifi Strength: " + new_firefighter_data["wifi_strength"])
        view_data["wifi_strength_var"].set(new_firefighter_data["wifi_strength"])
        view_data["last_updated_var"].set(new_firefighter_data["last_updated"])

        # Apply color to wifi strength and last updated based on the values
        # self.apply_color_to_wifi_strength(firefighter_id)
    
    def apply_color_to_wifi_strength(self, firefighter_id):
        # Access view representation data
        view_data = self.view_data[firefighter_id]
        wifi_strength_var = view_data["wifi_strength_var"]
        # get index of the wifi strength label
        
        wifi_strength_label = view_data["frame"].winfo_children()[9]  # Assuming wifi strength label is the 5th widget
        wifi_strength_value = wifi_strength_var.get()

        # view_data = self.view_data[firefighter_id]
        # wifi_strength_var = view_data["wifi_strength_var"]
        # wifi_strength_label = view_data.get("wifi_strength_label")  # Retrieve the Wi-Fi strength label widget


        # Apply color based on wifi strength value
        if "Excellent" in wifi_strength_value:
            wifi_strength_label.config(fg="green")
        elif "Good" in wifi_strength_value:
            wifi_strength_label.config(fg="blue")
        elif "Fair" in wifi_strength_value:
            wifi_strength_label.config(fg="orange")
        elif "Poor" in wifi_strength_value:
            wifi_strength_label.config(fg="red")


    # def create_firefighter_data_widgets(self, tab_frame):
    #     self.rendered_firefighters = demo_firefighter_data# get_demo_firefighter_data()
        
    #     for firefighter in self.rendered_firefighters:
    #         self.create_firefighter_widget(tab_frame, firefighter)
    #         self.update_firefighter_widget(firefighter)
    #         # self.apply_color_to_wifi_strength(firefighter)

    # def create_firefighter_widget(self, tab_frame, firefighter):
    #     divider = ttk.Separator(tab_frame, orient="horizontal")
    #     divider.pack(fill="x")
        
    #     firefighter["gesture_var"] = tk.StringVar(value="None")
    #     firefighter["wifi_strength_var"] = tk.StringVar(value="None")
    #     firefighter["last_updated_var"] = tk.StringVar(value="None")
    #     firefighter["frame"] = tk.Frame(tab_frame)
    #     firefighter["frame"].pack()
        
    #     labels = [
    #         ("Name", firefighter["name"]),
    #         ("Location", firefighter["location"]),
    #         ("Gesture", firefighter["gesture_var"]), # mutable variable
    #         ("ID", firefighter["id"]),
    #         ("Wifi Strength", firefighter["wifi_strength_var"]), # mutable variable
    #         ("Last Updated", firefighter["last_updated_var"]) # mutable variable
    #     ]
        
    #     for label_text, label_value in labels:
    #         label = tk.Label(firefighter["frame"], text=label_text + ": ", anchor="e")
    #         label.pack(side=tk.LEFT)
    #         value_label = tk.Label(firefighter["frame"], textvariable=label_value)
    #         value_label.pack(side=tk.LEFT)
    #         firefighter[label_text.lower() + "_label"] = value_label

    # def update_firefighter_widget(self, firefighter):
    #     # Update dynamic values
        
    #     firefighter["gesture_var"].set(firefighter["gesture"])
    #     firefighter["wifi_strength_var"].set("Wifi Strength: " + firefighter["wifi_strength"])
    #     firefighter["last_updated_var"].set("Last Updated: {} seconds ago".format(firefighter["last_updated"]))


    # def apply_color_to_wifi_strength(self, firefighter):
    #     # Access the label widget associated with the StringVar
    #     wifi_strength_label = firefighter["wifi_strength_label"]

    #     # Retrieve the value from "wifi_strength_var"
    #     wifi_strength_var = firefighter["wifi_strength_var"]
    #     wifi_strength_value = wifi_strength_var.get()

    #     # Apply color based on the value
    #     if "Excellent" in wifi_strength_value:
    #         wifi_strength_label.config(fg="green")
    #     elif "Good" in wifi_strength_value:
    #         wifi_strength_label.config(fg="blue")
    #     elif "Fair" in wifi_strength_value:
    #         wifi_strength_label.config(fg="orange")
    #     elif "Poor" in wifi_strength_value:
    #         wifi_strength_label.config(fg="red")


    #     # color code the timing of the last update, if it is more than 10 seconds ago, make it red
    #     if firefighter["last_updated"] > 50:
    #         firefighter["last_updated_var"].config(fg="red")
    #     elif firefighter["last_updated"] > 20:
    #         firefighter["last_updated_var"].config(fg="orange")
    #     else:
    #         firefighter["last_updated_var"].config(fg="green")
    
    # def update_firefighter_widgets(self, new_firefighter_data):
    # # Assume new_firefighter_data is a list of dictionaries containing updated firefighter data
    
    #     for i, new_firefighter in enumerate(new_firefighter_data):
    #         rendered_firefighter = self.rendered_firefighters[i]  # Get the corresponding rendered firefighter data
            
    #         # Update the StringVar objects with new data
    #         rendered_firefighter["gesture_var"].set(new_firefighter["gesture"])
    #         rendered_firefighter["wifi_strength_var"].set("Wifi Strength: " + new_firefighter["wifi_strength"])
    #         rendered_firefighter["last_updated_var"].set("Last Updated: {} seconds ago".format(new_firefighter["last_updated"]))
            # self.apply_color_to_wifi_strength(rendered_firefighter)
        # Optionally, update other dynamic values in the widget if necessary
        # apply_color_to_wifi_strength
        # Optionally, apply any formatting or color changes based on the new data



    def create_matplotlib_plot(self, tab_frame):
        # Create a figure
        # f = plt.Figure(figsize=(5,4), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 2, 3, 13, 4, 1, 2])
        
        # # Create a canvas for the figure
        # self.canvas = FigureCanvasTkAgg(f, tab_frame)
        # self.canvas.draw()
        # self.canvas_widget = self.canvas.get_tk_widget()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        # self.firefighter_labels = []
        # self.firefighter_data = []

        # self.fig, self.ax = plt.subplots()
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab1)
        # self.canvas_widget = self.canvas.get_tk_widget()
        # self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        # self.firefighter_labels = []
        # self.firefighter_data = []
    ### TAB 3 FUNCTIONS ###
        
    def create_record_gestures_widgets(self, tab_frame):
        # Folder selection
        self.folder_label = tk.Label(tab_frame, text="Select Gesture Folder:")
        self.folder_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.folder_var = tk.StringVar()
        self.folder_entry = tk.Entry(tab_frame, textvariable=self.folder_var, width=40)
        self.folder_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        self.browse_button = tk.Button(tab_frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        # Gesture name entry
        self.gesture_label = tk.Label(tab_frame, text="Enter Gesture Name:")
        self.gesture_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.gesture_name_var = tk.StringVar()
        self.gesture_name_entry = tk.Entry(tab_frame, textvariable=self.gesture_name_var, width=40)
        self.gesture_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        # Record button
        self.record_button = tk.Button(tab_frame, text="Record Gesture", command=self.record_gesture)
        self.record_button.grid(row=2, column=1, padx=10, pady=5, sticky="we")

        self.stop_record_button = tk.Button(tab_frame, text="Stop Recording", command=self.stop_record_gesture)
        self.stop_record_button.grid(row=2, column=2, padx=10, pady=5, sticky="we")

        # Recording status
        self.recording_text = tk.StringVar()
        self.recording_text.set("Not Recording")
        self.recording_label = tk.Label(tab_frame, textvariable=self.recording_text)
        self.recording_label.grid(row=3, column=1, padx=10, pady=5, sticky="we")

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory(initialdir=".", title="Select Gesture Folder")
        print("Selected folder:", self.folder_path)
        if self.folder_path:
            self.folder_var.set(self.folder_path)
            print(f"Selected folder: {self.folder_path}")

    def record_gesture(self):
        gesture_name = self.gesture_name_var.get()
        print("GESTURE NAME:", gesture_name)
        folder_path = self.folder_var.get()
        print("folder path:", folder_path)
        if gesture_name and folder_path and not self.recording:
            self.recording = True
            self.recording_text.set(f"Completed Recording Gesture in folder '{folder_path}'")
            gesture_folder = os.path.join(folder_path, gesture_name)
            print(f"Gesture '{gesture_name}' recorded in folder '{gesture_folder}'")
        else:
            self.recording_text.set("Not Recording")
            print("Please enter both gesture name and select a folder.")

    def stop_record_gesture(self):
        self.recording = False
        self.recording_text.set("Not Recording")


        
        # Create a grid of labels in tab 2
        # self.render_firefighter_data()


        # for idx, firefighter in enumerate(demo_firefighter_data):
        #     firefighter_frame = tk.Frame(self.root)
        #     firefighter_frame.grid(row=idx, column=0, padx=10, pady=5)
            
        #     name_label = tk.Label(firefighter_frame, text=firefighter["name"])
        #     name_label.grid(row=0, column=0, padx=5, pady=5)
            
        #     gesture_label = tk.Label(firefighter_frame, textvariable=firefighter["gesture"])
        #     gesture_label.grid(row=0, column=1, padx=5, pady=5)
        
        # make a grid that iterates over the firefighter objects and will display the data
        # for firefighter in firefighters:
        #     print(firefighter.name)
        # Connect to the server
   

        # Start receiving data
        # self.receive_data()
    def render_firefighter_data(self):
        # each firefighter will have a name, location, and gesture
        tk.Label(self.tab2, text="Firefighter Data").pack()

        for firefighter in self.rendred_firefighters:
            print("Rendering firefighter data")
            print("firefighter", firefighter)
            # turn the firefighter into a dictionary
            # firefighter = dict(firefighter)
            # create new keys for the firefighter
            # rendered["id"]+=1
            firefighter["gesture"] = tk.StringVar()
            firefighter["gesture"].set("None")
            firefighter["frame"] = tk.Frame(self.tab2)
            firefighter["frame"].pack()
            firefighter["name_label"] = tk.Label(firefighter["frame"], text=firefighter["name"])
            firefighter["name_label"].pack()
            firefighter["location_label"] = tk.Label(firefighter["frame"], text=firefighter["location"])
            firefighter["location_label"].pack()
            firefighter["gesture_label"] = tk.Label(firefighter["frame"], textvariable=firefighter["gesture"])
            firefighter["gesture_label"].pack()
            firefighter["id"] = tk.Label(firefighter["frame"], text=firefighter["id"])
            
            # rendered["id"] = str(int(rendered["id"])+1)
            # rendered["id"] = tk.Label(rendered["frame"], text=str(int(rendered["id"])+1))
            # increment id by 1 



    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                print("Received data:", data)
                # pass
                # data_dict = json.loads(data)
                self.refresh_data()
            # catch all errors
            except Exception as e:
                print("Connection to the server closed")
                # try to reconnect
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.server_host, self.server_port))
                # continue
                # break
            self.update_labels([])
        
            # data = self.client_socket.recv(1024).decode()
            # print("Received data:", data)
            # data_dict = json.loads(data)
            # self.update_labels(data_dict["data"])
            # self.refresh_data()

    def refresh_data(self):
        # self.client_socket.sendall("Refresh".encode())
        # self.root.after(1000, self.refresh_data)
        self.root.update_idletasks()
        self.root.update()
    
    # def update_firefighter_data(self, data):
    #     self.firefighter_data = data
    #     for firefighter in self.firefighter_data:
    #         firefighter["gesture"] = tk.StringVar()
    #         firefighter["gesture"].set("None")

    def update_labels(self, data):
        # strength = data["strength"]
        # names = data["names"]
        # locations = data["locations"]
        # self.strength_label.config(text=f"Bluetooth/Wi-Fi Strength: {strength}")
        # self.names_label.config(text=f"Firefighter Names: {names}")
        # self.locations_label.config(text=f"Firefighter Locations: {locations}")
        # self.time_label.config(text=f"Time: {time.ctime()}")
        # update firefighter data
        # self.render_firefighter_data()
        for firefighter in get_demo_firefighter_data():
            # pass
            firefighter_id = firefighter["id"]
            self.update_firefighter_widget(firefighter_id, firefighter)
            # firefighter["gesture"].set("None")
        # self.update_firefighter_widget()
        # self.render_firefighter_data()
        # print("Updated labels")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    # run the receive_data method in a separate thread
    receive_data_thread = threading.Thread(target=app.receive_data)
    # run the thread in daemon mode so that it automatically stops when the main program exits
    receive_data_thread.daemon = True
    receive_data_thread.start()
    # run tk in main loop

    root.mainloop()

# User
# I want to have a matplotlib chart within a tab named "realtime mesh network structure"
# I want it to use the lsit of firefighters, and show how the networks are chained together.  I want my computer to be seen as the abse station, and each firefighter should be a node thats connecting. Make this a function as this will be changing in real time, and the tree/graph structure will change 