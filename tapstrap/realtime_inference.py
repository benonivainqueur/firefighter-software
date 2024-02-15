from joblib import load
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
# import threading
from tapsdk import TapSDK, TapInputMode
from tapsdk.models import AirGestures
import os
import asyncio
# import platform
# import logging
from bleak import _logger as logger
# import sys
# import json
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.signal import find_peaks
from tabulate import tabulate
import time
from .tools import feature_extraction, table, on_linux, rolling_feature_extraction, reshape_data
# from tapstrap_gesture_recorder import average_and_create_payload
from .tapstrap_interpolated import merge_packets
from .tools import connect_to_tapstrap
import queue
global shared_queue 
shared_queue = queue.Queue(maxsize=10)

# on_linux = False
# # use os package to determine if we are on a form of linux
# on_linux = on_linux()

# check if we are on ubuntu

    
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
    predictions = []
    
    if lstm: 
        df = df.dropna()
        df = reshape_data(df, window_size=100, use_label=False)
        # print("df shape", df)
        start = time.time()
        try:
            predictions = loaded_model.predict(df)
       
            end = time.time()
            inf_time = end - start
            # use three decimal places
            # inf_time = round(inf_time, 3)
            print(inf_time,"s")
            print("sparse", predictions)
            print("predictions",  np.argmax(predictions, axis=1))
            # print("raw predictions", predictions)
            # print("pred " ,predictions[0])
            pred = predictions[0]
            max = -100
            max_index = -1
            for i in range(len(pred)):
                if pred[i] > max:
                    max = pred[i]
                    max_index = i
        except Exception as e:
            print(e)
            print("error in inference")
        # print("max index", max_index)

        # print("argmax", np.argmax(pred))
        # predictions = np.argmax(predictions[0])
        # get index of max value
        # for i in range(len(predictions)):
        #     predictions[i] = np.argmax(predictions[i])
        # predictions = np.bincount(predictions).argmax()
        # print("predictions:", predictions, "shape", predictions.shape())
        # print("pred",predictions)
        # print(" most likely prediction", np.bincount(predictions).argmax())
        # return predictions
        # time.sleep(2)

    else: 
        # start timer to see how long it takes to perform inference
        df = df.fillna(0)        
        start = time.time()
        predictions = loaded_model.predict(df)
        end = time.time()
        inf_time = end - start
        # use three decimal places
        inf_time = round(inf_time, 3)
        print("predictions:", predictions, "inf_time:", inf_time,"s")

    # except Exception as e:
    #     print(e)
    #     print("error in inference")
    if len(predictions) == 0:
        return -1
    else: 
        return predictions[0]
    
   

# def on_raw_data_no_thumb(identifier, packets):
#     if  (on_raw_data.accel_cnt >= 200 or on_raw_data.imu_cnt >= 200):
#         on_raw_data.accel_cnt = 0
#         on_raw_data.imu_cnt = 0
#         # print("performing inference")
#         new_df = process_accelerometer_data(timestamped_accel_values)
#         feature_df = feature_extraction(new_df, use_label=False,normalize=True)
#         perform_inference(feature_df)
#         # clear out the arrays
#         timestamped_accel_values.clear()
#         timestamped_imu_values.clear()
#         print(timestamped_accel_values)
#     else: 
#         for m in packets:
#             if m["type"] == "imu":
#                 timestamped_imu_values.append(m["payload"])
#                 on_raw_data.imu_cnt += 1
#             if m["type"] == "accl":
#                 timestamped_accel_values.append(m["payload"])
#                 on_raw_data.accel_cnt += 1

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
            if (lstm == True):
                feature_df = rolling_feature_extraction(new_df, use_label=False, interpolated = use_thumb, normalize=True)
            else:  
                feature_df = feature_extraction(new_df, use_label=False, interpolated = use_thumb, normalize=True)
            inference = perform_inference(feature_df)
            shared_queue.put((inference,time.time()))
            # if (int == 1 and client != None):
            #     print("vibrate")
            reset_arrays()
        else:
            # new_df = process_accelerometer_data(timestamped_accel_values)
            # feature_df = feature_extraction(new_df, use_label=False, normalize=True)
            # val = perform_inference(feature_df)
            # reset_arrays()
            pass
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


# async def run(loop, debug=False):
#     print("beginning run looop")
#     if debug:
#         # loop.set_debug(True)
#         l = logging.getLogger("asyncio")
#         l.setLevel(logging.DEBUG)
#         h = logging.StreamHandler(sys.stdout)
#         h.setLevel(logging.INFO)
#         l.addHandler(h)
#         logger.addHandler(h)

#     client = TapSDK(loop)
#     # devices = await client.list_connected_taps()
#     x = await client.manager.connect_retrieved()
#     x = await client.manager.is_connected()
#     logger.info("Connected: {0}".format(x))

#     await client.set_input_mode(TapInputMode("raw", sensitivity=[0,0,0]))
#     await client.register_raw_data_events(on_raw_data)
#     await client.send_vibration_sequence([100,100,100])
#     # await asyncio.sleep(3)
#     # await client.send_vibration_sequence([100, 200])
#     await asyncio.sleep(run_time, True) # this line  is to keep the program running for 50 seconds

on_raw_data.imu_cnt = 0
on_raw_data.accel_cnt = 0
on_raw_data.interpol_cnt = 0  

timestamped_accel_values = []
timestamped_imu_values = []
timestamped_interpolated_values = []
polling_window = 50 # how many readings we need to perform feature extraction and inference
client = None # global variable that will hold the client

# 
def main(headless = False):
   
   
    # print current directory
    while True:
        # print("hello!")
        shared_queue.put(("0",time.time()))
        # shared_queue.put(time.time())
        # put in delay 
        time.sleep(1)
        # put time in queue 
        
    # time.sleep(1)
    print(os.getcwd())
    use_thumb = True # decides whether or not to use the thumb in the feature extraction
    run_time = 200.0 # how long the program will run for
    # get current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # get the name of each model under the model directory
    # models = ["KNeighborsClassifier", "LogisticRegression", "RandomForestClassifier", "SVC"]
    models = os.listdir(current_dir + "/models/")
    # remove .DS_Store from the list
    if ".DS_Store" in models:
        models.remove(".DS_Store")
    # use list comprehension to map a index to a model name 
    model_tuples = [(models[i], i) for i  in range(len(models))]
    if headless:
       
        model_num = 2
    else: 
        model_num = input("Enter model number. {models}:".format(models=model_tuples))
    model_path = current_dir+'/models/{m}'.format(m = model_tuples[int(model_num)][0])
    print("Using model: {m}".format(m = model_tuples[int(model_num)][0]))
    
    # check if the model is an lstm
    lstm = False
    if "lstm" in model_path:
        lstm = True
        # load the lstm model
        from keras.models import load_model
        loaded_model = load_model(model_path)
    else:
        # load the model
        loaded_model = joblib.load(model_path)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(connect_to_tapstrap(loop,on_raw_data,100))
        # loop.run_until_complete(run(loop, True))
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        loop.close()
    except Exception as e:
        print(e)
        loop.close()

if __name__ == "__main__":
    main()
    


