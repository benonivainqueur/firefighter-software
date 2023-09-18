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

def OnRawData(identifier, packets):
    if is_recording:
        # number of imu packets 
        # print(packets)
        # print("single packet: ", packets)
        number_of_msg_in_packet = len(packets)
        print("number_of_msg_in_packet", number_of_msg_in_packet)
        averaged_packet = merge_packets(packets, prexisting=False, remove_label=False, collecting_data=True)
        for p in averaged_packet:
            merged_values.append([p["ts"], p["payload"]])
        # merged_values.append([for packet in interpolated_packets[packet["ts"], packet["payload"]]])
        for m in packets:
            OnRawData.cnt += 1
            if m["type"] == "imu":
                    timestamped_imu_values.append([m["ts"], m["payload"]])
                    OnRawData.imu_cnt += 1
            if m["type"] == "accl":
                    timestamped_accel_values.append([m["ts"], m["payload"]])
                    OnRawData.accel_cnt += 1
           

OnRawData.imu_cnt = 0
OnRawData.accel_cnt = 0
OnRawData.cnt = 0

def record_data():
    global is_recording
    while True:
        gesture_name = input("Enter the name of the gesture (or 'quit' to quit): ")
        # gesture_name = 'Turn'
        if gesture_name.lower() == 'quit':
            # is_recording = False
            print("Quitting...")
            # exit the program
            sys.exit(0)
            exit()
            break
        else:
            global timestamped_imu_values
            global timestamped_accel_values

            timestamped_imu_values = []
            timestamped_accel_values = []

            is_recording = True
            print("Start recording, press ctrl+c to stop recording...")
            while is_recording:
                # print a message very 5 iterations 
                if OnRawData.imu_cnt % 5 == 0:
                    print("Recording...", OnRawData.imu_cnt)
                time.sleep(0.1)
            # if the owrd turn is in the gesture name, then set the label to 1
            if gesture_name.lower().find('turn') != -1:
                label = 1

            if gesture_name.lower().find('still') != -1:
                label = 0
            
            if gesture_name.lower().find('lever') != -1:
                label = 2

            base_path = './interpolated_data'
            # TODO - Refactor this into a function
            if gesture_name.lower().find('turn') != -1:
                # Find the highest numbered folder with the name containing "Turn"
                folder_name_pattern = r'Turn(\d+)'
                existing_folders = [folder for folder in os.listdir(base_path) if re.match(folder_name_pattern, folder)]
                if existing_folders:
                    # Get the highest number from the existing folders
                    existing_numbers = [int(re.search(folder_name_pattern, folder).group(1)) for folder in existing_folders]
                    highest_number = max(existing_numbers)
                    next_number = highest_number + 1
                else:
                    next_number = 1

                # Create the new folder with the incremented number
                folder_name = f'Turn{next_number}'

            elif gesture_name.lower().find('still') != -1:
                # Find the highest numbered folder with the name containing "Turn"
                folder_name_pattern = r'Still(\d+)'
                existing_folders = [folder for folder in os.listdir(base_path) if re.match(folder_name_pattern, folder)]
                if existing_folders:
                    # Get the highest number from the existing folders
                    existing_numbers = [int(re.search(folder_name_pattern, folder).group(1)) for folder in existing_folders]
                    highest_number = max(existing_numbers)
                    next_number = highest_number + 1
                else:
                    next_number = 1

                # Create the new folder with the incremented number
                folder_name = f'Still{next_number}'
            elif gesture_name.lower().find('lever') != -1:
                # Find the highest numbered folder with the name containing "Turn"
                folder_name_pattern = r'lever(\d+)'
                existing_folders = [folder for folder in os.listdir(base_path) if re.match(folder_name_pattern, folder)]
                if existing_folders:
                    # Get the highest number from the existing folders
                    existing_numbers = [int(re.search(folder_name_pattern, folder).group(1)) for folder in existing_folders]
                    highest_number = max(existing_numbers)
                    next_number = highest_number + 1
                else:
                    next_number = 1

                # Create the new folder with the incremented number
                folder_name = f'lever{next_number}'
            else:
                folder_name = gesture_name

            folder_path = os.path.join(base_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            imu_file_path = os.path.join(folder_path, 'thumb_imu_data.json')
            accel_file_path = os.path.join(folder_path, 'fingers_accel_data.json')           

            # Save recorded data
          
            # os.makedirs(f'{base_path}/{gesture_name}', exist_ok=True)
            # imu_file_path = f'{base_path}/{gesture_name}/imu_data.json'
            # accel_file_path = f'{base_path}/{gesture_name}/accel_data.json'

            # Save recorded data

            # interpolate the timestamped_imu_values and timestamped accel valuess

            # TODO: Refactor this into a function
            with open(imu_file_path, 'w') as f:
                for imu_data in timestamped_imu_values:
                    json.dump({'timestamp':  imu_data[0], 'payload':  imu_data[1], 'label': label}, f)
                    f.write('\n')
                # json.dump(timestamped_imu_values, f)
            with open(accel_file_path, 'w') as f:
                for accel_data in timestamped_accel_values:
                # json.dump(timestamped_accel_values, f)
                    json.dump({'timestamp':  accel_data[0], 'payload':  accel_data[1], 'label': label}, f)
                    f.write('\n')

            interpolation_file_path = os.path.join(folder_path, 'interpolated_data.json')  
            with open(interpolation_file_path, 'w') as f:
                for interpolated in merged_values:
                # json.dump(timestamped_accel_values, f)
                    json.dump({'timestamp':  interpolated[0], 'payload':  interpolated[1], 'label': label}, f)
                    f.write('\n')         

            # interpolate_and_save(imu_file_path, accel_file_path, interpolation_file_path,label )

            print(f"Data saved to {imu_file_path} and {accel_file_path}")
            print("# IMU packets recieved: ", OnRawData.imu_cnt)
            print("# IMU Entries", len(timestamped_imu_values))
            print("# Accel packets recieved: ", OnRawData.accel_cnt)
            print("# Aceel Entries", len(timestamped_accel_values))
            print("# interpolated packets recieved: ", OnRawData.accel_cnt)
            print("# interpolated Entries", len(merged_values))



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
   
    import time
    # do not start the record_thread for three seconds
    # time.sleep(3)
    record_thread = threading.Thread(target=record_data)
    record_thread.start()
    await asyncio.sleep(1000.0, True) 
    # after the 100 seconds, print a message saying that the program is done
    print("\nCommunication with TapStrap Closed. ")
    # open_channel = False
    exit()


    # await asyncio.sleep(10.0, True) # this line  is to keep the program running for 50 seconds


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop, True))
