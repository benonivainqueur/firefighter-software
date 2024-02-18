sudo apt-get install -y batctl

# copy the data from start-batman-adv.sh to /etc/batman-setup.sh
sudo cp ./start-batman-adv.sh ~/start-batman-adv.sh

chmod +x ~/start-batman-adv.sh

sudo cp ./wlan0.txt /etc/network/interfaces.d/wlan0

echo 'batman-adv' | sudo tee --append /etc/modules

echo 'denyinterfaces wlan0' | sudo tee --append /etc/dhcpcd.conf