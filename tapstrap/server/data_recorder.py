import pathlib
import socket
import time
import threading

data_files_path = pathlib.Path(__file__).parent.resolve() / "raw_train_data"


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8888))
sock.listen(1)

# Only deal with taking in one connection for now
conn, addr = sock.accept()
run_threads = True


def write_data_to_file(filename):
    global run_threads
    with open(filename, "w+") as file:
        while run_threads:
            buf = conn.recv(8196)
            if len(buf) > 0:
                txt = buf.decode('ascii')
                file.write(txt)


# build file with timestamps of when we start/end a gesture
# on training, the data segment between the timestamps is labeled
# as a gesture and every other segment is not
def run_hand_recording():
    global data_files_path
    input("Start data recording")
    session_time = int(time.time() * 1000)  # use millisecond time
    tmp_file = data_files_path / ("tmp_" + str(session_time) + ".txt")
    print("tmp file: " + str(tmp_file))

    recorder_thread = threading.Thread(target=write_data_to_file, args=(tmp_file,))
    recorder_thread.start()
    gesture_dict = dict()  # map gesture name to start/end tuple

    gesture_name = input("Name your gesture: ")
    while gesture_name != "":
        if gesture_name in gesture_dict:
            print("We already have a gesture named that.")
            gesture_name = input("Enter next gesture: ")
            continue
        input("Press enter when you start your gesture.")
        start_time = int(time.time() * 1000)  # use millisecond time
        end_time = start_time + 10000

        print(f"Started at {start_time}, will end recording at {end_time}")
        time.sleep(10)
        print(f"Finished gesture {gesture_name}")
        gesture_dict[gesture_name] = (start_time, end_time)
        gesture_name = input("Enter next gesture: ")

    global run_threads
    run_threads = False
    recorder_thread.join()
    gestures_ordered = sorted(gesture_dict, key=lambda g: gesture_dict[g][0])

    print("Done recording, parsing temp file")
    with open(tmp_file, "r") as data_file:
        gesture_files = {gesture: open(data_files_path / f"{gesture}_{session_time}.txt", "w+") for gesture in gesture_dict}
        for line in data_file:
            if "|" not in line:
                continue
            timestamp, data = line.split("|")
            timestamp = eval(timestamp)

            for g in gesture_dict:
                start, end = gesture_dict[g]
                if start <= timestamp < end:
                    gesture_files[g].write(line)
                    break
        for g in gesture_dict:
            gesture_files[g].close()
    print(f"Finished recording {len(gesture_dict)} gestures.")

run_hand_recording()