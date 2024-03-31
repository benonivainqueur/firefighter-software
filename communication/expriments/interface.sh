# start interface
# takes in a string, either olsr or batman
# ping $IP for 3 seconds

start_interface() {
    # echo "Starting interface.... recieving $1 as argument."
    if [ "$1" == "olsr" ]; then
        cd ~/firefighter-software/scripts
        ./start_olsr.sh
    elif [ "$1" == "batman" ]; then
        cd ~/firefighter-software/scripts
        ./start_batman.sh
    elif [ "$1" == "iperf" ]; then
        # cd ~/firefighter-software/scripts
        ./run_iperf.sh
    elif [ "$1" == "ping" ]; then
        # cd ~/firefighter-software/scripts
        ./fping.sh 10 bat0
    else
        echo "Invalid interface type. Please enter either 'olsr' or 'batman'."
    fi
}
# stop interface
start_interface $1 
# ping -c 3 172.27.0.0 
# ping -c 50 -s 16 -i 0.5 172.27.0.0 -I bat0 
