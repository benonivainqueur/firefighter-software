import tkinter as tk
from tkinter import ttk

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Firefighter Dashboard")
        self.root.geometry("600x400")

        # Label for Bluetooth/Wi-Fi strength
        self.strength_label = ttk.Label(root, text="Bluetooth/Wi-Fi Strength:")
        self.strength_label.pack()

        # Label for firefighter names
        self.names_label = ttk.Label(root, text="Firefighter Names:")
        self.names_label.pack()

        # Label for firefighter locations
        self.locations_label = ttk.Label(root, text="Firefighter Locations:")
        self.locations_label.pack()

        # Button to refresh data
        self.refresh_button = ttk.Button(root, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.pack()

    def refresh_data(self):
        # Update Bluetooth/Wi-Fi strength label
        # (You can replace this with actual data retrieval logic)
        self.strength_label.config(text="Bluetooth/Wi-Fi Strength: Excellent")

        # Update firefighter names label
        # (You can replace this with actual data retrieval logic)
        self.names_label.config(text="Firefighter Names: John, Sarah, Michael")

        # Update firefighter locations label
        # (You can replace this with actual data retrieval logic)
        self.locations_label.config(text="Firefighter Locations: Building A, Floor 2")

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
