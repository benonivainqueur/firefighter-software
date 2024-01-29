from scapy.all import *
from scapy.all import sniff, IP, ICMP, sr1
import time

print(get_if_list())

# print("test", Dot11)
def packet_handler(packet):
    # if packet.haslayer(Dot11):
    print("packet type, ", packet.type)
    if packet.type == 0 and packet.subtype == 8:  # Type 0 (Management frame), Subtype 8 (Beacon frame)
        print(f"SSID: {packet.info.decode('utf-8')}, Signal Strength: {packet.dBm_AntSignal}")
# list all the wifi interfaces
#
# # Sniff Wi-Fi traffic
# sniff(iface='en0', prn=packet_handler)

# def process_packet(packet):
#     print(packet.summary())

# sniff(iface='en0', prn=process_packet, filter='ip', count=10)
# get time to live
# print(IP().ttl)


import subprocess
import re

# def get_signal_strength(interface):
#     try:
#         cmd = subprocess.Popen(['ifconfig', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         output = cmd.communicate()[0]
#         signal_level = re.search(r"Signal level=(-\d+)", output.decode('utf-8'))
#         if signal_level:
#             return int(signal_level.group(1))
#         else:
#             return None
#     except Exception as e:
#         print("Error:", e)
#         return None


# # Specify your WiFi interface name
# interface_name = "en0"  # Change this to your interface name
# signal_strength = get_signal_strength(interface_name)

# if signal_strength is not None:
#     print("Signal Strength:", signal_strength, "dBm")
# else:
#     print("Unable to retrieve signal strength.")

import subprocess
import re

def get_signal_strength():
    try:
        cmd = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = cmd.communicate()[0]
        signal_level = re.search(r"CtlRSSI: (-\d+)", output.decode('utf-8'))
        if signal_level:
            return int(signal_level.group(1))
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

import subprocess
import re

def get_network_info():
    try:
        cmd = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = cmd.communicate()[0].decode('utf-8')

        # Regular expressions to extract specific network information
        ssid_match = re.search(r"SSID: (.+)", output)
        bssid_match = re.search(r"BSSID: (.+)", output)
        channel_match = re.search(r"channel: (\d+)", output)
        security_match = re.search(r"link auth: (.+)", output)
        signal_level_match = re.search(r"CtlRSSI: (-\d+)", output)

        # Extracted values or None if not found
        ssid = ssid_match.group(1) if ssid_match else None
        bssid = bssid_match.group(1) if bssid_match else None
        channel = int(channel_match.group(1)) if channel_match else None
        security = security_match.group(1) if security_match else None
        signal_level = int(signal_level_match.group(1)) if signal_level_match else None

        return {
            "SSID": ssid,
            "BSSID": bssid,
            "Channel": channel,
            "Security": security,
            "Signal Strength (dBm)": signal_level
        }
    except Exception as e:
        print("Error:", e)
        return None

while True: 
    time.sleep(.5)
    network_info = get_network_info()

    if network_info is not None:
        print("Network Information:")
        for key, value in network_info.items():
            print(f"{key}: {value}")
    else:
        print("Unable to retrieve network information.")



def custom_packets(): 

    # Create an IP packet object. Set the destination IP address.
    ip_packet = IP(dst="8.8.8.8")

    # Create an ICMP packet object.
    icmp_packet = ICMP()

    # Combine the IP and ICMP objects to create a complete packet.
    packet = ip_packet/icmp_packet

    # Send the packet and capture the response.
    response = sr1(packet)

    # Print the response.
    print(response.show())  