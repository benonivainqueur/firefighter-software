
# sudo su
echo 'export ff="/home/pi1/firefighter-software"' >> ~/.bashrc
# sudo chmod a+x *.sh
sudo apt-get update && sudo apt-get upgrade -y &&
sudo apt-get install -y python3-pip && sudo apt-get install batctl &&
git config --global --add safe.directory /home/pi1/firefighter-software 
cd /home/pi1/firefighter-software/etc
pip install -r python-deps.txt
cd /home/pi1

# tapstrap stuff 
sudo apt-get install bluez-tools libbluetooth-dev
sudo usermod -G bluetooth -a $USER
#and can reload groups in this shell by running the following command or by logging out and back in:
su - $USER
cd /home/pi1

git clone https://github.com/TapWithUs/tap-python-sdk.git
cd tap-python-sdk
pip install .


