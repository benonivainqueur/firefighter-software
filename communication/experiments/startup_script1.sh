#!/bin/bash
# this script is going to run at startup time. it will wait for the network to be up and running
# then it will pull the latest code from the git repository. Then it will run another script called start up 2
# cd ~/firefighter-software/scripts
# ./restart_networking.sh
cd ~/firefighter-software/communication/experiments

# Function to check Wi-Fi connection status, and keep checking until it is successful
check_wifi_connection() {
    if ping -q -c 1 -W 1 google.com >/dev/null; then
        return 0 # Connection successful
    # else if to see if the device is connected to the network
    elif ifconfig wlan0 | grep -q "inet addr:"; then
        return 0 # Connection successful
    # else if connected to bat0
    elif ifconfig bat0 | grep -q "inet addr:"; then
        return 0 # Connection successful
    else
        return 1 # Connection failed
    fi
}

# Wait for Wi-Fi connection
# use a counter to try 5 times 
# if the connection is not successful, then exit the script
counter=0
while ! check_wifi_connection; do
    echo "Waiting for Wi-Fi connection..."
    sleep 1 # Adjust the sleep duration as needed
    counter=$((counter+1))
    if [ $counter -eq 5 ]; then
        echo "Connection failed. Exiting."
        # break out of the loop, but still continue with the script
        break
        
    fi
done


# Wi-Fi connection detected, proceed with further commands

# Pull the latest code from the git repository
cd ~/firefighter-software
git pull

# Run the startup 2 script

# cd ~/firefighter-software/communication/experiments
# $INTERFACE
cd ~/firefighter-software/scripts
# run iwconfig, if bat0 is not found, then run batman.sh

./batman.sh

cd ~/firefighter-software/communication/experiments #&& python3 client.py

