# could be a different command if you are using a different OS on your RPi
sudo systemctl stop NetworkManager 
sleep .5
# Use your own interface name if its not wlan1
sudo iwconfig wlan0 mode Ad-Hoc
sleep .5
# Use your own interface name if its not wlan1
# you can change the name of your network here
sudo iwconfig wlan0 essid "TurtleAdHoc"
sleep .5

###############################################
# EDIT MADE HERE
# you will need a unique IP address for each device in your mesh network
# you should keep all of them in the same subnet. 
# I had my IP address in the 192.168.7.xxx subnet
###############################################
# Use your own interface name if its not wlan1
# sudo ifconfig wlan1 192.168.7.3 netmask 255.255.255.0 up
sudo ifconfig wlan0 172.27.0.$PI_ID/16  netmask 255.255.255.0 up
sleep .5
#sudo olsrd -i wlan1

sudo olsrd -i wlan0 -r olsr.conf