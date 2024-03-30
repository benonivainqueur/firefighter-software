# run the iperf3 server

# if the $RP_IP is equal to 0, run iperf3 server, else run iperf3 client
if [ $PI_ID -eq 0 ]; then
    iperf3 -s -p 54321
else
    # ping the server for 3 seconds to check if the server is up
    
    iperf3 -c 172.27.0.0 -p 54321 -t 10 -J --bidir --timestamps  -i 0.5
    #   iperf3 -c 172.27.0.0 -p 54321 -t 10 -J --bidir --timestamps > iperf_client.txt
    
fi


# send the iperf_client.txt file to the server 
# scp iperf_client.txt pi1@$172.27.0.0:~/iperf_client.txt
# will ask for password
# password is raspberry
# echo "iperf_client.txt file sent to the server"

# iperf3 -c 172.27.0.0 -p 54321 -t 30 -J --bidir --timestamps > test.txt

