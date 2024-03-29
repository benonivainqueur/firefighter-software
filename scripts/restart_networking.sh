sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode managed 
sudo systemctl restart NetworkManager
# kill batman-adv
sudo modprobe -r batman-adv
# kill olsrd
sudo killall olsrd
