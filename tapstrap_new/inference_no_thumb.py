from joblib import load
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
import os
import asyncio
import logging
from bleak import _logger as logger
import sys
import pandas as pd
import sys
import numpy as np
from tools import feature_extraction

os.environ["PYTHONASYNCIODEBUG"] = str(1)


accel_values = []
imu_values = []


# Load the saved model
# get current directory
current_dir = os.path.dirname(os.path.realpath(__file__))
# print(current_dir)

# Define list of fingers
fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

# List to hold features
features = ['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 
            'middle_x', 'middle_y', 'middle_z', 'ring_x', 'ring_y', 'ring_z', 
            'pinky_x', 'pinky_y', 'pinky_z']

new_features = ['imu_x', 'imu_y', 'imu_z', 'imu_p','imu_y', 'imu_r'] + features
print(new_features)

real_time_data = pd.DataFrame(columns=features)  # Initialize an empty dataframe with feature column names


# whenever we hit 50 reads from the accelerometer, we will kick off the feature extraction process
# we will then append the features to the real-time data dataframe
def process_accelerometer_data(accel_values):
    # turn the accelerometer data into a dataframe
    # print(accel_values)
    # new_data = {}
    # turn list into dataframe
    # for imu_data in timestamped_accel_values:
        # make a new dictionary to store the data
        # loop through the data and add it to the dictionary
        # new_data.update({'payload': imu_data[0]})

    columns = ['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 'middle_x', 'middle_y', 'middle_z',
           'ring_x', 'ring_y', 'ring_z', 'pinky_x', 'pinky_y', 'pinky_z']

    df = pd.DataFrame(accel_values, columns=columns)
    # print(df)
    # print('NEW DATA DONE PRINTING')
    # print("imu data length", len (imu_values))
  
    return df

def perform_inference(df):

    predictions = loaded_model.predict(df)
    print("predictions:", predictions)

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


# def OnGesture(identifier, gesture):
#     print(str(identifier) + " gesture " + str(AirGestures(gesture)))


def OnTapConnected(self, identifier, name, fw):
    print(str(identifier) + " Tap: " + str(name), " FW Version: ", fw)


def OnTapDisconnected(self, identifier):
    print(str(identifier) + " Tap: " + identifier + " disconnected")


def OnMoused(identifier, vx, vy, isMouse):
    print(str(identifier) + " mouse movement: %d, %d, %d" %(vx, vy, isMouse))

timestamped_accel_values = []
timestamped_imu_values = []

def OnRawData(identifier, packets):
    if  (OnRawData.accel_cnt >= 200 or OnRawData.imu_cnt >= 200):
        OnRawData.accel_cnt = 0
        OnRawData.imu_cnt = 0
        print("performing inference")
        new_df = process_accelerometer_data(timestamped_accel_values)
        feature_df = feature_extraction(new_df, use_label=False)
        perform_inference(feature_df)
        # clear out the arrays
        timestamped_accel_values.clear()
        timestamped_imu_values.clear()
        print(timestamped_accel_values)
        # timestamped_accel_values = []
        # timestamped_imu_values = []
        # os.sleep(1)
    else: 
        for m in packets:
            if m["type"] == "imu":
                timestamped_imu_values.append(m["payload"])
                OnRawData.imu_cnt += 1
            if m["type"] == "accl":
                timestamped_accel_values.append(m["payload"])
                OnRawData.accel_cnt += 1
        
OnRawData.imu_cnt = 0
OnRawData.accel_cnt = 0
OnRawData.cnt = 0

# create a function that will handle the incoming data
# parse the incoming data, and visualize the information in real time using a external library
# use accel and imu values and print 


async def run(loop, debug=False):
    print("beginning run looop")
    if debug:

        # loop.set_debug(True)
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.INFO)
        l.addHandler(h)
        logger.addHandler(h)
    
    client = TapSDK(loop)
    # devices = await client.list_connected_taps()
    x = await client.manager.connect_retrieved()
    x = await client.manager.is_connected()
    logger.info("Connected: {0}".format(x))

    await client.set_input_mode(TapInputMode("controller"))
    await client.register_raw_data_events(OnRawData)
    # await client.register_mouse_events(OnMoused)
    # await client.register_air_gesture_state_events(OnMouseModeChange)
    
    await asyncio.sleep(3)
    await client.set_input_mode(TapInputMode("raw", sensitivity=[0,0,0]))
    await client.send_vibration_sequence([100, 200])

    await asyncio.sleep(200.0, True) # this line  is to keep the program running for 50 seconds
    # record_thread = threading.Thread(target=perform_inference)
    # record_thread.start()
    # await asyncio.sleep(1000.0, True) 


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    use_interpolation = False

    model_path ='./firefighter-software/tapstrap_new/models/RandomForestClassifier_0.pkl'
    loaded_model = joblib.load(model_path)
    # setting up stubs for code cleanup, to run with either the interpolation trained models, or not 
    if use_interpolation:
        loop.run_until_complete(run(loop, True))

    loop.run_until_complete(run(loop, True))

# while True:
    # Read new accelerometer data
    # Process the data and extract required features
    # new_data = process_accelerometer_data()
    # features = final_feature_extraction(new_data)


    # Append the features to the real-time data dataframe
    # real_time_data = real_time_data.append(features, ignore_index=True)




