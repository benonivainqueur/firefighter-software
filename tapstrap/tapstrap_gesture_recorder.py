import time
import json
import threading
import signal
import asyncio
import logging
import time
import os
import re
import platform
import sys
import pandas as pd
from bleak import _logger as logger
from tools import feature_extraction, table, merge_packets
from tapsdk.models import AirGestures
from tapsdk import TapSDK, TapInputMode

os.environ["PYTHONASYNCIODEBUG"] = str(1)
# signal handler function called when SIGINT is received
def signal_handler(sig, frame):
    global is_recording
    is_recording = False
signal.signal(signal.SIGINT, signal_handler)
# setup signal handler for SIGINT (ctrl+c)

global is_recording
# Flag to control recording
is_recording = False
label= 1 # this label will signify the gesture that is being recorded
# Set signal handler for SIGINT (ctrl+c)
counter = 0
# Lists to store data
timestamped_imu_values = []
timestamped_accel_values = []
merged_values = []
global first_iteration
first_iteration = True
global base_path
base_path = 'tapstrap/training_data/finger_taps'

def OnRawData(identifier, packets):
    if is_recording:
        # number_of_msg_in_packet = len(packets)
        # print("number_of_msg_in_packet", number_of_msg_in_packet)
        averaged_packet = merge_packets(packets, prexisting=False, remove_label=False, collecting_data=True)
        for p in averaged_packet:
            merged_values.append([p["ts"], p["payload"]])
            OnRawData.merge_cnt += 1
        # merged_values.append([for packet in interpolated_packets[packet["ts"], packet["payload"]]])
        for m in packets:
            if m["type"] == "imu":
                    timestamped_imu_values.append([m["ts"], m["payload"]])
                    OnRawData.imu_cnt += 1
            if m["type"] == "accl":
                    timestamped_accel_values.append([m["ts"], m["payload"]])
                    OnRawData.accel_cnt += 1
           

OnRawData.imu_cnt = 0
OnRawData.accel_cnt = 0
OnRawData.merge_cnt = 0

# gesture list 
# label_tuples = [('turn', 1), ('still',0), ('lever',2)]
# label_tuples = {'turn': 1, 'still':0 , 'lever':2}
label_tuples = {}

# add a new entry to the dictionary
first_iteration = True

def get_next_folder_num(gesture_name):
    folder_name_pattern = '{gesture_name}(\d+)'.format(gesture_name=gesture_name)
    print("gesture_name", gesture_name)
    print("folder_count", folder_count)
    if folder_count[gesture_name] == -1 or first_iteration or gesture_name not in folder_count.keys(): 
        existing_folders = [folder for folder in os.listdir(base_path) if re.match(folder_name_pattern, folder)]
        if (len(existing_folders) == 0):
             folder_count[gesture_name]  = folder_count[gesture_name] + 1
             return folder_count[gesture_name]
        else :
            existing_numbers = [int(re.search(folder_name_pattern, folder).group(1)) for folder in existing_folders]
            folder_count[gesture_name] = max(existing_numbers) + 1
            return folder_count[gesture_name]
    else : 
        # add new entry to the dictionary
        folder_count[gesture_name]  += 1
        return folder_count[gesture_name]
    
 

def file_writer(file_path, data, label):
    with open(file_path, 'w') as f:
        for values in data:
            # throwing error here
            json.dump({'timestamp':  values[0], 'payload':  values[1], 'label': int(label)}, f)
            f.write('\n')

def get_folder_label(folder_name):
    # open the json file and get the label
    folder_path = os.path.join(base_path, folder_name)
    # print("folder_path", folder_path)
    # open json file
    with open(os.path.join(folder_path, 'imu_data.json'), 'r') as f:
        imu_data = [json.loads(line) for line in f]
    imu_df = pd.DataFrame(imu_data)
    label = imu_df['label'].iloc[0]
    return label 

# set folder_tuples
def set_folder_tuples(existing_folders, passed_folder_count):
    for folder in existing_folders:
        # ignore folders that are empty
        if folder not in label_tuples.keys():
            label = get_folder_label(folder+ "1")
            label_tuples[folder] = label
            folder_count[folder] = passed_folder_count[folder]
            print("folder_count[{folder}]".format(folder=folder), folder_count[folder])
            # folder_count[folder] = folder_num


def record_data():
    global is_recording
    global folder_count 
    # include only folders
    existing_folders = [folder for folder in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder))]
    # remove numbers from each folder name
    existing_folders = [re.sub(r'\d+', '', folder) for folder in existing_folders]
    # for each unique folder name, get the number of folders with that name
    # folder_count = {'turn': -1, 'still':-1 , 'lever':-1}
    folder_count = {folder: existing_folders.count(folder) for folder in existing_folders}
    print ("folder_count", folder_count)
    existing_folders = list(set(existing_folders))# get the unique folder names, i.e, our gestures 
    set_folder_tuples(existing_folders, folder_count)
    print("set folder tuples", label_tuples)
    # if len(existing_folders) == 0:
    #     print("No existing folders")
    # else:
    #     print("existing_folders", existing_folders)
    #     print("folder_count", folder_count)
    # for folder in existing_folders:
    #     if folder in folder_count.keys():
    #         folder_count[folder] = -1p
    print("existing_folders", existing_folders)
    # if no existing folders, ask for a folder name, and create a new folder
    # if len(existing_folders) == 0:
    #     folder_name = input("No existing folders.. enter the name of the gesture (or 'quit' to quit): ").lower()
    #     if folder_name.lower() == 'quit':
    #         # is_recording = False
    #         print("Quitting...")
    #         return
    #     else:
    #         # add new entry to the dictionary
    #         folder_count[folder_name] = 0
    #         label_tuples[folder_name] = 0
    #         # folder_count[folder_name] = 0
    #         # label_tuples[folder_name] = 0
    old_gesture_name = ''
    auto_mode = False
    print("Type 'auto' and your gesture name following it to enable auto mode... 'auto wave' for example")
    while True:
        # if (not automate_collection):
        if not auto_mode:
            gesture_name = input("Enter the name of the gesture (or 'quit' to quit). (press enter to continue to keep the previous gesture name) ").lower()
        if gesture_name == '' and old_gesture_name != '':
            print("using previous gesture name of {0}".format(old_gesture_name))
            gesture_name = old_gesture_name
        else:
            old_gesture_name = gesture_name
        # gesture_name = 'lever'
        if 'auto' in gesture_name.lower() :
            auto_mode = True
            gesture_name = gesture_name.split(' ')[1]
            print("Auto mode enabled")

        is_recording = True
        
        # gesture_name = 'Turn'
        if gesture_name.lower() == 'quit':
            # is_recording = False
            print("Quitting...")
            return 
        else:
            global timestamped_imu_values
            global timestamped_accel_values
            global merged_values
            timestamped_imu_values = []
            timestamped_accel_values = []
            merged_values = []
            OnRawData.imu_cnt = 0
            OnRawData.accel_cnt = 0
            OnRawData.merge_cnt = 0
            is_recording = True
            # wait for 3 seconds before starting the recording
            # time.sleep(3) # this is a alternate way to 
            # make a time counter that will count down from 3 to 0
            #
            # sleep_time = 10
            print("press ctrl+c to stop recording...")
            # while (OnRawData.merge_cnt < 150):
            #     # this is to ensure that we have enough data to perform feature extraction and inference
            #     pass
            
            while is_recording:
                # print a message very 5 iterations 
                if OnRawData.imu_cnt % 5 == 0:
                    print("Recording...", OnRawData.imu_cnt)
                time.sleep(0.1)
            # if the owrd turn is in the gesture name, then set the label to 1
            # label = label_tuples[gesture_name.lower()]
            # base_path = './interpolated_data'
            if gesture_name not in folder_count.keys():
                print("adding a new gesture", gesture_name)
                # add new entry to the dictionary
                folder_count[gesture_name] = 0
                label_tuples[gesture_name] = len(label_tuples.keys())
            
            # gets the next folder number
            next_folder_num = get_next_folder_num(gesture_name)
            folder_name = f'{gesture_name}{next_folder_num}'
            folder_count[gesture_name] = next_folder_num
            label = label_tuples[gesture_name]
            folder_path = os.path.join(base_path, folder_name)
            os.makedirs(folder_path, exist_ok=False)
            imu_file_path = os.path.join(folder_path, 'imu_data.json')
            accel_file_path = os.path.join(folder_path, 'accel_data.json')  
            interpolation_file_path = os.path.join(folder_path, 'merged_data.json')

            # save the data to the folder
            file_writer(imu_file_path, timestamped_imu_values, label)
            file_writer(accel_file_path, timestamped_accel_values, label)
            file_writer(interpolation_file_path, merged_values, label)
       
            print(f"Data saved to {imu_file_path} and {accel_file_path} and {interpolation_file_path}")
            print("# Entries IMU:{} | Accel:{} | Interpolated {}".format(len(timestamped_imu_values), len(timestamped_accel_values), len(merged_values)))

def interpolate_and_save(imu_file_path, accel_file_path, output_file_path, label):
    # Load IMU data
    with open(imu_file_path, 'r') as f:
        imu_data = [json.loads(line) for line in f]
    imu_df = pd.DataFrame(imu_data)

    imu_df[['thumb_imu_x', 'thumb_imu_y', 'thumb_imu_z', 'thumb_imu_pitch', 'thumb_imu_yaw', 'thumb_imu_roll']] = pd.DataFrame(imu_df.pop('payload').values.tolist(), index=imu_df.index)
    imu_df['timestamp'] = pd.to_datetime(imu_df['timestamp'], unit='s')  # Convert to datetime
    imu_df = imu_df.groupby('timestamp').mean()

    # Load accelerometer data
    with open(accel_file_path, 'r') as f:
        accel_data = [json.loads(line) for line in f]
    accel_df = pd.DataFrame(accel_data)
    accel_df[['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 
            'middle_x', 'middle_y', 'middle_z', 'ring_x', 'ring_y', 'ring_z', 
            'pinky_x', 'pinky_y', 'pinky_z']] = pd.DataFrame(accel_df.pop('payload').values.tolist(), index=accel_df.index)
    accel_df['timestamp'] = pd.to_datetime(accel_df['timestamp'], unit='s')  # Convert to datetime
    accel_df = accel_df.groupby('timestamp').mean()

    # Merge accelerometer and IMU data
    merged_df = pd.concat([accel_df, imu_df], axis=1)


    # Resample to common frequency and interpolate missing values
    resampled_df = merged_df.resample('5ms').mean()  # 200Hz corresponds to a 5ms period
    interpolated_df = resampled_df.interpolate()  # Fill missing values using linear interpolation

    # Add label
    interpolated_df['label'] = label

    # Save interpolated data
    with open(output_file_path, 'w') as f:
        for timestamp, row in interpolated_df.iterrows():
            output_data = {'timestamp': timestamp.timestamp(), 'payload': row.drop('label').tolist(), 'label': row['label']}
            json.dump(output_data, f)
            f.write('\n')

async def run(loop, debug=False):
    if debug:
        import sys
        loop.set_debug(True)
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.INFO)
        l.addHandler(h)
        logger.addHandler(h)
    
    client = TapSDK(loop)
    x = await client.manager.connect_retrieved()
    x = await client.manager.is_connected()
    logger.info("Connected: {0}".format(x))

    # await client.set_input_mode(TapInputMode("controller"))
    await client.set_input_mode(TapInputMode("controller"))
    # await client.send_vibration_sequence([100, 200, 300, 400, 500])


    await client.register_raw_data_events(OnRawData)

    await asyncio.sleep(1)
    await client.set_input_mode(TapInputMode("raw", sensitivity=[0,0,0]))
    await client.send_vibration_sequence([300,100,300])
    #wait for three seconds
   
    # do not start the record_thread for three seconds
    # time.sleep(3)
    global record_thread 
    record_thread = threading.Thread(target=record_data)
    # end the thread 
    
    # when record_data returns, end the program
    # end_program = threading.Thread(target=exit) # this u
    record_thread.start()
    # break the asyncio loop when the thread is joined 
    # asyncio.run(loop)
    while True:
        if not record_thread.is_alive():
            break
        await asyncio.sleep(0.1)
    # await asyncio.sleep(1000.0) # this line  is to keep the program running for 50 seconds
    # await asyncio.gather(loop)
    record_thread.join()

    # after the 100 seconds, print a message saying that the program is done
    print("\nCommunication with TapStrap Closed. ")
    # open_channel = False
    exit()


    # await asyncio.sleep(10.0, True) # this line  is to keep the program running for 50 seconds

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop, True))
