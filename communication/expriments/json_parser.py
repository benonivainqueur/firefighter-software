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

