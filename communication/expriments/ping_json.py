import re
import json

def parse_data(data):
    result = {}
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) : \[(\d+)\], 64 bytes, (\d+\.\d+) ms \((\d+\.\d+) avg, (\d+)% loss\)')
    summary_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) : xmt/rcv/%loss = (\d+)/(\d+)/(\d+)%?, min/avg/max = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)')
    
    for match in ip_pattern.finditer(data):
        ip = match.group(1)
        index = int(match.group(2))
        latency = float(match.group(3))
        avg_latency = float(match.group(4))
        loss_percentage = int(match.group(5))
        if ip not in result:
            result[ip] = []
        result[ip].append({
            "index": index,
            "latency": latency,
            "avg_latency": avg_latency,
            "loss_percentage": loss_percentage
        })

    for match in summary_pattern.finditer(data):
        ip = match.group(1)
        transmitted = int(match.group(2))
        received = int(match.group(3))
        loss = int(match.group(4))
        min_latency = float(match.group(5))
        avg_latency = float(match.group(6))
        max_latency = float(match.group(7))
        result[ip].append({
            "transmitted": transmitted,
            "received": received,
            "loss": loss,
            "min_latency": min_latency,
            "avg_latency": avg_latency,
            "max_latency": max_latency
        })

    return json.dumps(result, indent=4)

# Example usage:
data = """
172.27.0.0 : [0], 64 bytes, 0.135 ms (0.135 avg, 0% loss)
172.27.0.1 : [0], 64 bytes, 6.07 ms (6.07 avg, 0% loss)
172.27.0.2 : [0], 64 bytes, 3.72 ms (3.72 avg, 0% loss)
172.27.0.3 : [0], 64 bytes, 3.28 ms (3.28 avg, 0% loss)
172.27.0.4 : [0], 64 bytes, 2.60 ms (2.60 avg, 0% loss)
172.27.0.5 : [0], 64 bytes, 4.34 ms (4.34 avg, 0% loss)
...
"""

# load data from ping.txt
with open("ping2.txt", "r") as f:
    data = f.read()
    print(data)

parsed_data = parse_data(data)
print(parsed_data)
