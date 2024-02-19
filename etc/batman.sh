# Activate batman-adv
sudo apt install libnl-3-dev libnl-genl-3-dev
sudo modprobe batman-adv
# Disable and configure wlan0
sudo ip link set wlan0 down
sudo ifconfig wlan0 mtu 1500
sudo iwconfig wlan0 mode ad-hoc
sudo iwconfig wlan0 essid my-mesh-network
# sudo iwconfig wlan0 ap 01:23:45:67:89:AB
sudo iwconfig wlan0 channel 8
sleep 1s
sudo ip link set wlan0 up
sleep 1s
sudo batctl if add wlan0
sleep 1s
sudo ifconfig bat0 up
sleep 2s
# Use different IPv4 addresses for each device
# This is the only change necessary to the script for
# different devices. Make sure to indicate the number
# of bits used for the mask.
# Prompt the user for the last octet of the IP address
read -p "Enter the last octet of the IP address for bat0 (0-255): " last_octet

# Construct the full IP address with the provided last octet
ip_address="172.27.0.$last_octet/16"

# Set the IP address for bat0
sudo ifconfig bat0 $ip_address

echo "bat0 configured with IP address: $ip_address"
# sudo ifconfig bat0 172.27.0.1/16
# print done
echo "batman-adv setup complete"