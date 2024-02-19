#!/bin/bash

# Define the BATMAN-adv mesh interface
BATMAN_IF="bat0"

# Bring up the wireless interface
ip link set up dev wlan0

# Add the wireless interface to the BATMAN-adv mesh
batctl if add wlan0

# Activate the BATMAN-adv mesh interface
ip link set up dev $BATMAN_IF

# Optional: Set the mesh interface MTU to 1532 bytes (adjust as needed)
ip link set mtu 1532 dev $BATMAN_IF

# Print information about the BATMAN-adv mesh
batctl meshif $BATMAN_IF

echo "Configuration completed."
