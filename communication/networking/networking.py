from scapy.all import *

def packet_handler(packet):
    if packet.haslayer(Dot11):
        if packet.type == 0 and packet.subtype == 8:  # Type 0 (Management frame), Subtype 8 (Beacon frame)
            print(f"SSID: {packet.info.decode('utf-8')}, Signal Strength: {packet.dBm_AntSignal}")

# Sniff Wi-Fi traffic
sniff(iface='wlan0', prn=packet_handler)
