# start interface
# takes in a string, either olsr or batman
start_interface() {
    echo "Starting interface.... recieving $1 as argument."
    if [ "$1" == "olsr" ]; then
        cd ~/firefighter-software/scripts
        ./start_olsr.sh
    elif [ "$1" == "batman" ]; then
        cd ~/firefighter-software/scripts
        ./start_batman.sh
    elif [ "$1" == "iperf" ]; then
        # cd ~/firefighter-software/scripts
        ./run_iperf.sh
    else
        echo "Invalid interface type. Please enter either 'olsr' or 'batman'."
    fi
}
# stop interface
start_interface $1
