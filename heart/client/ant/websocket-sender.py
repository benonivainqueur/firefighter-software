import threading

from ant.easy.node import Node
from ant.easy.channel import Channel
from websockets.sync.client import connect


NETWORK_KEY = [0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45]


def on_data_receive(data):
    print("RCVD: " + str(data))
    with connect('ws://192.168.0.28:8008') as websocket:
        websocket.send('a+' + str(data[-1]))


def thread_run(node):
    node.set_network_key(0x00, NETWORK_KEY)
    channel = node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE)
    channel.on_broadcast_data = on_data_receive
    channel.on_burst_data = on_data_receive

    channel.set_period(8070)
    channel.set_search_timeout(20)
    channel.set_rf_freq(57)
    channel.set_id(0, 120, 0)

    try:
        channel.open()
        node.start()
    finally:
        node.stop()
        print("node shutdown finished")


node = Node()
x = threading.Thread(target=thread_run, args=(node,))
x.start()
