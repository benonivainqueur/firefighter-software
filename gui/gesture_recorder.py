import tkinter as tk
from tkinter import filedialog
import os

class GestureRecorderApp:
    def __init__(self, master):
        self.master = master
        self.recording = False
        self.create_record_gestures_widgets()

    def create_record_gestures_widgets(self):
        tab_frame = tk.Frame(self.master)
        tab_frame.pack()

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
        folder_path = filedialog.askdirectory(initialdir=".", title="Select Gesture Folder")
        if folder_path:
            self.folder_var.set(folder_path)

    def record_gesture(self):
        gesture_name = self.gesture_name_var.get().strip()
        folder_path = self.folder_var.get()
        if gesture_name and folder_path and not self.recording:
            gesture_folder = os.path.join(folder_path, gesture_name)
            try:
                os.makedirs(gesture_folder)
                self.recording = True
                self.recording_text.set(f"Recording Gesture in folder '{gesture_folder}'")
            except OSError as e:
                self.recording_text.set(f"Error: {e}")
        elif self.recording:
            self.recording_text.set("Already Recording")
        else:
            self.recording_text.set("Please enter gesture name and select a folder.")

    def stop_record_gesture(self):
        if self.recording:
            self.recording = False
            self.recording_text.set("Not Recording")

root = tk.Tk()
app = GestureRecorderApp(root)
root.mainloop()
