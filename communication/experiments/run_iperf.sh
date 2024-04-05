# run the iperf3 server

# if the $RP_IP is equal to 0, run iperf3 server, else run iperf3 client
if [ $PI_ID -eq 0 ]; then
    iperf3 -s -p 54321 -J  --logfile iperf_log.txt  -i 0.1
else
    # ping the server for 3 seconds to check if the server is up
    
    # iperf3 -c 172.27.0.0 -p 54321 -t 3 -J --bidir --timestamps  -i 0.1
    iperf3 -c 172.27.0.0 -p 54321 -t 5 -J --timestamps  -i 0.1

    #   iperf3 -c 172.27.0.0 -p 54321 -t 10 -J --bidir --timestamps > iperf_client.txt
    
fi


