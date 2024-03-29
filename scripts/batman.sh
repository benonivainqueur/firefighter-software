#!/bin/bash

# Function to execute the batman-adv setup commands
setup_batman_adv() {
    sudo modprobe batman-adv
    sudo systemctl stop NetworkManager
    sleep 1s
    sudo ip link set wlan0 down
    sleep 1s
    sudo ifconfig wlan0 mtu 1478
    sudo iwconfig wlan0 mode ad-hoc
    sudo iwconfig wlan0 essid KLOG-AD-HOC # Change this to whatever you like
    sudo iwconfig wlan0 ap 02:12:34:56:78:9A
    sudo iwconfig wlan0 channel 1
    sleep 1s
    sudo ip link set wlan0 up
    sleep 1s
    sudo batctl if add wlan0
    sleep 1s
    sudo ifconfig bat0 up
    sleep 1s
    sudo ifconfig bat0 172.27.0.$PI_ID/16
}

# Function to execute the setup and handle errors
setup_with_retry() {
    local retry_count=0
    local max_retries=3
    local retry_delay=5

    while true; do
        if [ $retry_count -eq $max_retries ]; then
            echo "Reached maximum number of retries. Exiting."
            exit 1
        fi

        echo "Attempt $((retry_count + 1))"
        setup_batman_adv

        # Check if any error occurred
        if grep -q "Error" <<< "$output"; then
            echo "Error detected. Retrying in $retry_delay seconds..."
            ((retry_count++))
            sleep $retry_delay
        else
            echo "Setup successful."
            break
        fi
    done
}

# Run setup with retry
setup_with_retry
