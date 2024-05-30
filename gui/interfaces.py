

# we need to define common types that can be shared between the GUI and the clients. This will allow us to send messages back and forth between the server and the clients.

import time 

def calculate_time_diff(server_time, client_time):
    # calculate the time difference and latency with the most accuracy possible 
    # turn server time into milliseconds
    server_time = time.mktime(server_time)
    # turn client time into milliseconds
    client_time = time.mktime(client_time)
    # calculate the difference
    diff = server_time - client_time
    return diff

class MessageType:
    MESSAGE = 1
    TIME_SYNC = 2
    TIME_DIFF = 3
    TIME_SYNC_ACK = 4

class Message:
    def __init__(self, sender, receiver, message: MessageType):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def __str__(self):
        return f"Sender: {self.sender}, Receiver: {self.receiver}, Message: {self.message}"
    

