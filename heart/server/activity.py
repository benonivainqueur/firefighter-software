from websockets.sync.client import connect
WEB_SOCKET_ADDR = "ws://172.20.10.2:8008"
started = False


def get_status():
    global started
    if started:
        started = False
        return "END"
    else:
        started = True
        return "START"


with connect(WEB_SOCKET_ADDR) as websocket:
    while True:
        go = input()
        if go == "s":
            msg = get_status()
            websocket.send(msg)
            print(msg)
        elif go == "t":
            msg = "TURN"
            websocket.send(msg)
            print(msg)