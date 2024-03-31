import re
import json

def parse_data(data):
    # result = {}
    # ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) : \[(\d+)\], 64 bytes, (\d+\.\d+) ms \((\d+\.\d+) avg, (\d+)% loss\)')
    # summary_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) : xmt/rcv/%loss = (\d+)/(\d+)/(\d+)%?, min/avg/max = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)')

    # for match in ip_pattern.finditer(data):
    #     ip = match.group(1)
    #     index = int(match.group(2))
    #     latency = float(match.group(3))
    #     avg_latency = float(match.group(4))
    #     loss_percentage = int(match.group(5))
    #     if ip not in result:
    #         result[ip] = []
    #     result[ip].append({
    #         "index": index,
    #         "latency": latency,
    #         "avg_latency": avg_latency,
    #         "loss_percentage": loss_percentage
    #     })

    # for match in summary_pattern.finditer(data):
    #     ip = match.group(1)
    #     transmitted = int(match.group(2))
    #     received = int(match.group(3))
    #     loss = int(match.group(4))
    #     min_latency = float(match.group(5))
    #     avg_latency = float(match.group(6))
    #     max_latency = float(match.group(7))
    #     result[ip].append({
    #         "transmitted": transmitted,
    #         "received": received,
    #         "loss": loss,
    # #         "min_latency": min_latency,
    # #         "avg_latency": avg_latency,
    # #         "max_latency": max_latency
    # #     })
    # pattern = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*:\s*\[(?P<index>\d+)\],\s*(?P<size>\d+) bytes,\s*(?P<time>\S+)\s+ms\s+\((?P<avg>\S+)\s+avg,\s*(?P<loss>\S+)% loss\)')

    # # Match the pattern for each line and store the results in a list of dictionaries
    # results = []
    # for match in pattern.finditer(data):
    #     results.append(match.groupdict())

    # # Convert the list of dictionaries to JSON format
    # json_data = json.dumps(results, indent=4)
    # print(json_data)
    # Regular expression pattern to match each line
    pattern = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*:\s*\[(?P<index>\d+)\],\s*(?P<size>\d+) bytes,\s*(?P<time>\S+)\s+ms\s+\((?P<avg>\S+)\s+avg,\s*(?P<loss>\S+)% loss\)')

    # Match the pattern for each line and store the results in a dictionary
    results = {}
    for match in pattern.finditer(data):
        ip = match.group('ip')
        index = int(match.group('index'))
        size = int(match.group('size'))
        time = float(match.group('time'))
        avg = float(match.group('avg'))
        loss = float(match.group('loss'))

        if ip not in results:
            results[ip] = []

        results[ip].append({
            'index': index,
            'size': size,
            'time': time,
            'avg': avg,
            'loss': loss
        })

    min_ip = None   
    min_time = 1000000
    for ip, data in results.items():
        for d in data:
            if d["time"] < min_time:
                min_time = d["time"]
                min_ip = ip

    print("IP address with the smallest minimum time:", min_ip)

    # Convert the dictionary to JSON format
    json_data = json.dumps(results, indent=4)
    print(json_data)
        # iterate through the minimum latencies, and whichever is the minimum latency, that is the ip address

        # for ip, data in result.items():
        #     min_latency = 1000000
        #     for d in data:
        #         if d["min_latency"] < min_latency:
        #             min_latency = d["min_latency"]
        #             result[ip] = d

        # client_id = result["destination_ip"][-1]
        # num_files = len([f for f in os.listdir("./data/pi" + client_id) if f.endswith('.json')])
    # with open("./data/pi" + client_id + "/ping" + str(num_files) + ".json", "w") as f:
        # f.write(json.dumps(result, indent=4))
    # j = json.dumps(result, indent=4)
    # print(j)
    # print("test")
        


    # return json.dumps(result, indent=4)

# Example usage:
# data = """
# 172.27.0.0 : [0], 64 bytes, 0.135 ms (0.135 avg, 0% loss)
# 172.27.0.1 : [0], 64 bytes, 6.07 ms (6.07 avg, 0% loss)
# 172.27.0.2 : [0], 64 bytes, 3.72 ms (3.72 avg, 0% loss)
# 172.27.0.3 : [0], 64 bytes, 3.28 ms (3.28 avg, 0% loss)
# 172.27.0.4 : [0], 64 bytes, 2.60 ms (2.60 avg, 0% loss)
# 172.27.0.5 : [0], 64 bytes, 4.34 ms (4.34 avg, 0% loss)
# ...
# """

# load data from ping.txt
with open("ping2.txt", "r") as f:
    data = f.read()
    # print(data)


import json

# Define a function to parse the output and create a dictionary
def parse_output(output):
    lines = output.strip().split('\n')
    data = {}
    for line in lines:
        if line:
            parts = line.split(' : ')
            ip = parts[0]
            # details = parts[1].strip('[]').split(', ')
            # seq_no = int(details[0]) if details[0] != '' else None
            # bytes_received = int(details[1]) if details[1] != '' else None
            # rtt = float(details[2].split(' ')[0]) if details[2] != '' else None
            # avg_rtt = float(details[3].split(' ')[1][:-5]) if len(details) > 3 and details[3] != '' else None
            # packet_loss = float(details[3].split(' ')[3][:-1]) if len(details) > 3 and details[3] != '' else None
            # if ip not in data:
            #     data[ip] = []
            # data[ip].append({
            #     'seq_no': seq_no,
            #     'bytes_received': bytes_received,
            #     'rtt': rtt,
            #     'avg_rtt': avg_rtt,
            #     'packet_loss': packet_loss
            # })
    return data
data = ""
with open("ping2.txt", "r") as f:
    data = f.read()
# Parse the sample outputs and convert them to JSON
# outputs = [doc['document_content'] for doc in documents]
json_data = []
output = data
# for output in outputs:
# data = parse_output(output)
    # json_data.append(data)

# Print the JSON data
# for d in json_data:
    # print(json.dumps(d, indent=2))
# parsed_data = parse_data(data)
# print(parsed_data)
    
def final_parsed_data(data):
    data  = data.split("\n")
    result = {}
    print(data)
