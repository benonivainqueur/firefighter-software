#! /bin/sh
sudo modprobe batman-adv
sudo systemctl stop dhcpcd.service
sudo systemctl stop NetworkManager
sleep 1s
# Activate batman-adv
# Disable and configure wlan0
sudo ip link set wlan0 down
sleep 1s
sudo ifconfig wlan0 mtu 1478
sudo iwconfig wlan0 mode ad-hoc
sudo iwconfig wlan0 essid KLOG-AD-HOC # Change this to whatever you like
sudo iwconfig wlan0 ap 02:12:34:56:78:9A
sudo iwconfig wlan0 channel 1

# Enable port forwarding
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o bat0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i bat0 -o eth0 -j ACCEPT

sleep 1s
sudo ip link set wlan0 up

#iwconfig wlan0 essid KLOG-AD-HOC # Uncomment this if you are using a Rasp Pi 1 and have issues with essid not being created

sleep 1s
sudo batctl if add wlan0
sleep 1s
sudo ifconfig bat0 up
sleep 1s

# Use different IPv4 addresses for each device
sudo ifconfig bat0 172.27.0.$PI_ID/16 
