import json

# parse thoug hthe json 
def parse_ping_output(ping_output):
    # Split ping output into lines
    lines = ping_output.split('\n')

    # Extract statistics line
    statistics_line = lines[-2]

    # Split statistics line into fields
    statistics_fields = statistics_line.split(',')

    # Extract relevant statistics
    packet_loss = statistics_fields[2].split()[0]
    min_rtt = statistics_fields[3].split()[0]
    avg_rtt = statistics_fields[4].split()[0]
    max_rtt = statistics_fields[5].split()[0]
    mdev = statistics_fields[6].split()[0]

    # Return parsed statistics
    return {
        'packet_loss': packet_loss,
        'min_rtt': min_rtt,
        'avg_rtt': avg_rtt,
        'max_rtt': max_rtt,
        'mdev': mdev
    }

# clean ping
def clean_ping_output(ping_output):
    import re
    import json

    # Given text
    text = """PING 172.27.0.0 (172.27.0.0) 56(84) bytes of data.\n64 bytes from 172.27.0.0: icmp_seq=1 ttl=64 time=34.9 ms\n64 bytes from 172.27.0.0: icmp_seq=2 ttl=64 time=28.8 ms\n64 bytes from 172.27.0.0: icmp_seq=3 ttl=64 time=3.54 ms\n\n--- 172.27.0.0 ping statistics ---\n3 packets transmitted, 3 received, 0% packet loss, time 2002ms\nrtt min/avg/max/mdev = 3.539/22.420/34.936/13.584 ms\n"""

    # Regular expressions to extract relevant data
    pattern_ping = r'PING ([\d.]+) \(([\d.]+)\) (\d+)\((\d+)\) bytes of data.'
    pattern_stats = r'(\d+) packets transmitted, (\d+) received, (\d+)% packet loss, time (\d+)ms\nrtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms'

    # Extract relevant information
    ping_match = re.match(pattern_ping, text)
    stats_match = re.search(pattern_stats, text)

    # Construct dictionary with extracted data
    ping_data = {
        "destination": ping_match.group(1),
        "destination_ip": ping_match.group(2),
        "bytes_sent": int(ping_match.group(3)),
        "bytes_received": int(ping_match.group(4)),
        "statistics": {
            "packets_transmitted": int(stats_match.group(1)),
            "packets_received": int(stats_match.group(2)),
            "packet_loss_percentage": int(stats_match.group(3)),
            "transmission_time": int(stats_match.group(4)),
            "rtt": {
                "min": float(stats_match.group(5)),
                "avg": float(stats_match.group(6)),
                "max": float(stats_match.group(7)),
                "mdev": float(stats_match.group(8))
            }
        }
    }

    # Convert dictionary to JSON
    json_data = json.dumps(ping_data, indent=4)
    print(json_data)


    # load data.json
def main():
    # # load test.json
    # with open('test.json') as f:
    #     data = json.load(f)
    # print(data["start"]["connected"][0]["local_host"][-1])
    # import os 
    # # get the number of files in the folder for the corresponding client
    # client_id = data["start"]["connected"][0]["local_host"][-1]
    # print("client_id:", client_id)
    # # get last number in the client id
    # # get the current folder structure
    # num_files = len(os.listdir("./data/pi" + client_id))
    # # create the file name for the json file
    # # save json to file called data.json
    # with open("./data/pi" + client_id + "/data" + str(num_files) + ".json", "w") as f:
    #     # save json_data
    #     json.dump(data, f,indent=4)
    # print(num_files)
    # # create 
    # # print()
    # load in ping.txt
    ping_output = ""
    with open('ping.txt') as f:
        ping_output = f.read()

    # print(ping_output)
    clean_ping_output(ping_output)
    # parse_ping_output()

   

main()
    # Parse ping output 
