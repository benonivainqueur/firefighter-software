

# Function to check Wi-Fi connection status
check_wifi_connection() {
    if ping -q -c 1 -W 1 google.com >/dev/null; then
        return 0 # Connection successful
    else
        return 1 # Connection failed
    fi
}

# Wait for Wi-Fi connection
while ! check_wifi_connection; do
    echo "Waiting for Wi-Fi connection..."
    sleep 5 # Adjust the sleep duration as needed
done

# Wi-Fi connection detected, proceed with further commands
echo "Wi-Fi connection detected. Running further commands..."
# Add your additional commands here
git pull 

cd ~/firefighter-software/scripts
./batman.sh

cd ~/firefighter-software/networking/experiments
python3 client.py





