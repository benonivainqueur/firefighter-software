import socket
import time
import pickle

# Create a socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 12345))

# Generate timestamped events
events = [{'timestamp': time.time(), 'data': 'event_data'}]

# Serialize and send data
data_to_send = pickle.dumps(events)
sock.send(data_to_send)

# Close the socket
sock.close()