#!/bin/bash

# Prompt user for new hostname
read -p "Enter the new hostname: " new_hostname

# Update hostname file
echo "$new_hostname" | sudo tee /etc/hostname > /dev/null

# Update hosts file
# sudo sed -i "s/127.0.1.1.*/127.0.1.1\t$new_hostname/" /etc/hosts

# Notify user
echo "Hostname updated to: $new_hostname"

sudo vi /etc/hosts

# Reboot to apply changes
# read -p "A reboot is required to apply the changes. Would you like to reboot now? (y/n): " choice
# if [[ $choice =~ ^[Yy]$ ]]; then
#     sudo reboot
# else
#     echo "Please reboot your system later to apply the changes."
# fi
