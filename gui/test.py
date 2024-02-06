import pywifi
from pywifi import const

def get_wifi_signal_strength(interface_name):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces() # Assuming there's only one Wi-Fi interface
    # choose wlan0
    for i in iface:
        if i.name() == "wlan0":
            iface = i
            break
    print("Interface:", iface.name())
    iface.scan()
    results = iface.scan_results()

    for result in results:
        if result.ssid == interface_name:
            return result.signal

    return None

# Example usage:
interface_name = "Your_WiFi_SSID"  # Change this to your actual Wi-Fi SSID
signal_strength = get_wifi_signal_strength(interface_name)
if signal_strength is not None:
    print("Wi-Fi signal strength:", signal_strength, "dBm")
else:
    print("Failed to get Wi-Fi signal strength.")
