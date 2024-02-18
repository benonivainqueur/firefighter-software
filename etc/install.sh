
# sudo su
echo 'export ff="/home/orangepi/firefighter-software"' >> ~/.bashrc
# sudo chmod a+x *.sh
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip
git config --global --add safe.directory /home/orangepi/firefighter-software
cd /home/orangepi/firefighter-software/etc
pip3 install -r python-deps.txt
cd /home/orangepi

# tapstrap stuff 
sudo apt-get install bluez-tools libbluetooth-dev
sudo usermod -G bluetooth -a $USER
#and can reload groups in this shell by running the following command or by logging out and back in:
su - $USER
cd /home/orangepi

git clone https://github.com/TapWithUs/tap-python-sdk.git
cd tap-python-sdk
pip install .


