from joblib import load
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import threading
from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
import os
import asyncio
import platform
import logging
from bleak import _logger as logger
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.signal import find_peaks
from tabulate import tabulate
import time
from tools import feature_extraction, table
# from tapstrap_gesture_recorder import average_and_create_payload
from tapstrap_interpolated import merge_packets
os.environ["PYTHONASYNCIODEBUG"] = str(1)

# List to hold features
old_features = ['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 
            'middle_x', 'middle_y', 'middle_z', 'ring_x', 'ring_y', 'ring_z', 
            'pinky_x', 'pinky_y', 'pinky_z']

features = ['thumb_imu_x', 'thumb_imu_y', 'thumb_imu_z', 'thumb_imu_pitch','thumb_imu_yaw', 'thumb_imu_roll'] + old_features
# print(features)

real_time_data = pd.DataFrame(columns=features)  # Initialize an empty dataframe with feature column names

def process_accelerometer_data(accel_values):
    # turn the accelerometer data into a dataframe
    df = pd.DataFrame(accel_values, columns=old_features)
    return df

# we will then append the features to the real-time data dataframe
def process_interpolated_data(interpolated_data):
    df = pd.DataFrame(interpolated_data, columns=features)
    return df

'''
    This function uses the current model that is loaded in, and performs inference on the given dataframe
    The dataframe should be a dataframe of features.
    The returned value is the prediction as a integer
'''
def perform_inference(df):
    predictions = loaded_model.predict(df)
    print("predictions:", predictions)
    return predictions[0]
    
        

def on_raw_data_no_thumb(identifier, packets):
    if  (on_raw_data.accel_cnt >= 200 or on_raw_data.imu_cnt >= 200):
        on_raw_data.accel_cnt = 0
        on_raw_data.imu_cnt = 0
        # print("performing inference")
        new_df = process_accelerometer_data(timestamped_accel_values)
        feature_df = feature_extraction(new_df, use_label=False)
        perform_inference(feature_df)
        # clear out the arrays
        timestamped_accel_values.clear()
        timestamped_imu_values.clear()
        print(timestamped_accel_values)
    else: 
        for m in packets:
            if m["type"] == "imu":
                timestamped_imu_values.append(m["payload"])
                on_raw_data.imu_cnt += 1
            if m["type"] == "accl":
                timestamped_accel_values.append(m["payload"])
                on_raw_data.accel_cnt += 1

'''
    clears out the arrays and resets the counters
'''
def reset_arrays():
    timestamped_accel_values.clear()
    timestamped_imu_values.clear()
    timestamped_interpolated_values.clear()
    on_raw_data.imu_cnt = 0
    on_raw_data.accel_cnt = 0
    on_raw_data.interpol_cnt = 0

'''
    Call-back function that is called when raw data is received from the tap
    Every time we receive raw data, we will append it to the timestamped_accel_values array
    
    We will then check if we have n values in the array, if we do, we will kick off the feature
    extraction process and then inference. 
'''
def on_raw_data(identifier, packets):
    if  (on_raw_data.interpol_cnt >= polling_window or on_raw_data.accel_cnt >= polling_window or on_raw_data.imu_cnt >= polling_window ):
        # print("performing inference")
        if use_thumb:
            new_df = process_interpolated_data(timestamped_interpolated_values)
            feature_df = feature_extraction(new_df, use_label=False, interpolated = use_thumb)
            int = perform_inference(feature_df)
            if (int == 1 and client != None):
              print("vibrate")
              
            reset_arrays()
        else:
            new_df = process_accelerometer_data(timestamped_accel_values)
            feature_df = feature_extraction(new_df, use_label=False)
            val = perform_inference(feature_df)
            reset_arrays()
    else: 
        # print("appending to arrays")
        ip = merge_packets(packets,False,remove_label=use_thumb)
        # print("ip", ip)
        for m in ip:
            # print("timestamp", m["ts"])
            timestamped_interpolated_values.append(m["payload"])
            on_raw_data.interpol_cnt += 1  
        if not use_thumb:
            for m in packets:
                # these arent timestamped
                if m["type"] == "imu":
                    timestamped_imu_values.append(m["payload"])
                    on_raw_data.imu_cnt += 1
                if m["type"] == "accl":
                    timestamped_accel_values.append(m["payload"])
                    on_raw_data.accel_cnt += 1


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
    # await client.set_input_mode(TapInputMode("controller"))
    # await client.register_mouse_events(OnMoused)
    # await client.register_air_gesture_state_events(OnMouseModeChange)
    # await asyncio.sleep(3)

    await client.set_input_mode(TapInputMode("raw", sensitivity=[0,0,0]))
    await client.register_raw_data_events(on_raw_data)
    await client.send_vibration_sequence([100,100,100])
    # await asyncio.sleep(3)
    # await client.send_vibration_sequence([100, 200])
    await asyncio.sleep(run_time, True) # this line  is to keep the program running for 50 seconds
  
on_raw_data.imu_cnt = 0
on_raw_data.accel_cnt = 0
on_raw_data.interpol_cnt = 0  

timestamped_accel_values = []
timestamped_imu_values = []
timestamped_interpolated_values = []
polling_window = 200 # how many readings we need to perform feature extraction and inference
client = None # global variable that will hold the client
if __name__ == "__main__":
    # print current directory
    print(os.getcwd())
    use_thumb = True # decides whether or not to use the thumb in the feature extraction
    run_time = 200.0 # how long the program will run for
    # get current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # get the name of each model under the model directory
    # models = ["KNeighborsClassifier", "LogisticRegression", "RandomForestClassifier", "SVC"]
    models = os.listdir(current_dir + "/models/")

    # use list comprehension to map a index to a model name 
    model_tuples = [(models[i], i) for i  in range(len(models))]
    # take input, 1 for KNN, 2 for Logistic Regression, 3 for Random Forest, 4 for SVM
    model_num = input("Enter model number. {models}:".format(models=model_tuples))
    model_path = 'firefighter-software/tapstrap_new/models/{m}'.format(m = model_tuples[int(model_num)][0])
    print("Using model: {m}".format(m = model_tuples[int(model_num)][0]))
    loaded_model = joblib.load(model_path)
    # # load in model
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(loop, True))
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        loop.close()
    except Exception as e:
        print(e)
        loop.close()

# while True:
    # Read new accelerometer data
    # Process the data and extract required features
    # new_data = process_accelerometer_data()
    # features = final_feature_extraction(new_data)


    # Append the features to the real-time data dataframe
    # real_time_data = real_time_data.append(features, ignore_index=True)




