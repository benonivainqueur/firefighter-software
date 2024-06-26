from joblib import load
import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
import joblib
# import threading
# from tapsdk import TapSDK, TapInputMode
# from tapsdk.models import AirGestures
import os
import asyncio
from bleak import _logger as logger
import pandas as pd
import sys
import numpy as np
# from scipy.signal import find_peaks
# from tabulate import tabulate
import time
import __init__
sys.path.append( sys.path[0] + "/..")

from tapstrap.tools import feature_extraction, rolling_feature_extraction, reshape_data, connect_to_tapstrap, rolling_feature_extraction2
# from tapstrap_gesture_recorder import average_and_create_payload
from tapstrap.tapstrap_interpolated import merge_packets
# from  import connect_to_tapstrap
import queue
global tap_device
global shared_queue 
global vibration_queue
vibration_queue= queue.Queue()
queue_size = 10
shared_queue = queue.LifoQueue() 
gesture_map = {
    0: "come_here",
    1: "ring_tap",
    2: "two_index_tap",  
    3: "fist_hand",
    4: "thumbs_down",
    5: "thumbs_up",
    6: "index_tap",
    7: "two_finger_point",
    8: "middle_tap",
    

    # 0: "THUMB TO INDEX",
    # 1: "FINGER TO PINKY",
    # 2: "FINGER TO INDEX",  
    # 3: "DOUBLE TAP",
    # 4: "REPEAT",
    # 5: "THUMB TO RING",
    # 6: "THUMBS DOWN",
    # 7: "REGROUP",
    # 8: "THUMBS UP",
    # 9:"NONE"
}

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
# debug_print(features)

real_time_data = pd.DataFrame(columns=features)  # Initialize an empty dataframe with feature column names

# def debug_debug_print(msg):
    
def process_accelerometer_data(accel_values):
    # turn the accelerometer data into a dataframe
    df = pd.DataFrame(accel_values, columns=old_features)
    return df

# we will then append the features to the real-time data dataframe
def process_interpolated_data(interpolated_data):
    df = pd.DataFrame(interpolated_data, columns=features)
    return df

def generate_histogram(predictions):
    histogram = {}
    
    # Count the occurrences of each prediction
    for p in predictions:
        for i, pred in enumerate(p):
            if i not in histogram:
                histogram[i] = 0
            histogram[i] += pred
    
    # Find the maximum count for scaling
    max_count = max(histogram.values())
    
    # Generate the histogram
    for i in histogram:
        histogram[i] = int(histogram[i] / max_count * 20)  # Scale to fit within 20 characters
    
    # Print the histogram
    debug_print("Prediction Histogram:")
    for i in histogram:
        debug_print(f"{gesture_map[i]}: {'*' * histogram[i]}")

'''
    This function uses the current model that is loaded in, and performs inference on the given dataframe
    The dataframe should be a dataframe of features.
    The returned value is the prediction as a integer
'''
def perform_inference(df):
    predictions = []
    
    if lstm: 
        start = time.time()
        # df = df.fillna(0)
        df = reshape_data(df, window_size=100, use_label=False)
        # take the last sequence of df 
        # df = df[-1:]
        # take the last 5 sequences
        # df = df[-5:]
        # take every other sequence
        # df = df[::5]
        # debug_print("df shape", df)
        debug_print("df shape", df.shape)
        try:
            # predictions = loaded_model.predict(df)
            if headless:
                predictions = loaded_model.predict(df,verbose=0)
            else:
                predictions = loaded_model.predict(df,verbose=1)
            # predictions = loaded_model.predict(df, batch_size=1, verbose=0, steps=1, callbacks=None, max_queue_size=10, workers=2, use_multiprocessing=True )
            end = time.time()
            inf_time = end - start
            # use three decimal places
            # inf_time = round(inf_time, 3)
            debug_print(inf_time,"s")
            # print("len predictions", len(predictions))
            # debug_print("sparse", predictions)
            # print out the predictions cleanly with clear decimal places
            preds = []
            for p in predictions:
                preds.append({i:round(p[i],3) for i in range(len(p))})
            
            generate_histogram(predictions)
            # make a histogram of bars indicating the distribution of the predictions
                # print({i:round(p[i],3) for i in range(len(p))})
            # debug_print(preds)
            # debug_print("predictions",  np.argmax(predictions, axis=1))
            likely_pred = np.bincount(np.argmax(predictions, axis=1)).argmax()
            debug_print("most likely prediction", gesture_map[np.bincount(np.argmax(predictions, axis=1)).argmax()])
            shared_queue.put((likely_pred, time.time()))
            # print("shared quiere size", shared_queue.qsize())
            # print("content of shared queue", shared_queue.queue)
            if shared_queue.qsize() > queue_size:
                # remove the oldest value, which will be the first value in the queue
                shared_queue.get()
            # debug_print("raw predictions", predictions)
            # debug_print("pred " ,predictions[0])
            pred = predictions[0]
            max = -100
            max_index = -1
            for i in range(len(pred)):
                if pred[i] > max:
                    max = pred[i]
                    max_index = i
        except Exception as e:
            debug_print(e)
            debug_print("error in inference")
        # debug_print("max index", max_index)

        # debug_print("argmax", np.argmax(pred))
        # predictions = np.argmax(predictions[0])
        # get index of max value
        # for i in range(len(predictions)):
        #     predictions[i] = np.argmax(predictions[i])
        # predictions = np.bincount(predictions).argmax()
        # debug_print("predictions:", predictions, "shape", predictions.shape())
        # debug_print("pred",predictions)
        # debug_print(" most likely prediction", np.bincount(predictions).argmax())
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
        # shared_queue.put((predictions[0],time.time()))
        # shared_queue.put((np.bincount(np.argmax(predictions, axis=1)).argmax(), time.time()))
        # print("shared quiere size", shared_queue.qsize())
        # print("content of shared queue", shared_queue.queue)
        # if shared_queue.qsize() > queue_size:
        #     shared_queue.get()
        debug_print("predictions:", predictions, "inf_time:", inf_time,"s")
        return predictions[0]

    # except Exception as e:
    #     debug_print(e)
    #     debug_print("error in inference")
    if len(predictions) == 0:
        return -1
    else: 
        return predictions[0]
    
   


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
    if  (on_raw_data.interpol_cnt >= polling_window ) :#or on_raw_data.accel_cnt >= polling_window or on_raw_data.imu_cnt >= polling_window ):
            debug_print("performing inference")
            # fill na values with 0
        # try:
            # if vibration_queue:
                # asyncio.run(connect_to_tapstrap.tap_client.send_vibration_sequence(sequence=vibration_queue.get()))

            if use_thumb:
                start_time = time.time()
                new_df = process_interpolated_data(timestamped_interpolated_values)
                
                if (lstm == True):
                    feature_df = rolling_feature_extraction2(new_df, use_label=False, interpolated = use_thumb, normalize=True)
                else:  
                    feature_df = feature_extraction(new_df, use_label=False, interpolated = use_thumb, normalize=True)
                # print("before perfomring inf, the amount of value sin our array is", len(feature_df))
                # print("interpol count", on_raw_data.interpol_cnt)
                inference = perform_inference(feature_df)
                # use a seperate thread to run inference so that we arent blocking the main thread
                # thread = threading.Thread(target=perform_inference, args=(feature_df,))
                # shared_queue.put((inference,time.time()))
                end_time = time.time()
                # debug_print("FE Time", end_time - start_time)
                # if (int == 1 and client != None):
                #     debug_print("vibrate")
                reset_arrays()
            else:
                # new_df = process_accelerometer_data(timestamped_accel_values)
                # feature_df = feature_extraction(new_df, use_label=False, normalize=True)
                # val = perform_inference(feature_df)
                # reset_arrays()
                pass
        # except Exception as e:
            # debug_print(e)
            # debug_print("error on_raw_data")
            # reset_arrays()
            # return -1
    else: 
        # debug_print("appending to arrays")
        ip = merge_packets(packets,False,remove_label=use_thumb)
        # debug_print("ip", ip)
        try: 
            for m in ip:
                # debug_print("timestamp", m["ts"])
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
        except Exception as e:
            debug_print(e)
            debug_print("error on_raw_data")


on_raw_data.imu_cnt = 0
on_raw_data.accel_cnt = 0
on_raw_data.interpol_cnt = 0  

timestamped_accel_values = []
timestamped_imu_values = []
timestamped_interpolated_values = []
polling_window =120 # how many readings we need to perform feature extraction and inference
client = None # global variable that will hold the client

def debug_print(*args):
    if headless: 
        # pass
        print(*args)
    else:
        print(*args)
    

def main(hl = False,async_loop=None):
    global headless 
    global use_thumb
    global run_time
    global loaded_model
    global lstm
    global tap_device
    headless = hl
    lstm = False
    use_thumb = True # decides whether or not to use the thumb in the feature extraction
    run_time = 10000000.0
    # debug_print current directory
    # while True:
    #     # debug_print("hello!")
    #     shared_queue.put(("0",time.time()))
    #     # shared_queue.put(time.time())
    #     # put in delay 
    #     time.sleep(1)
    #     # put time in queue 
        
    # time.sleep(1)
    # debug_print(os.getcwd())
     # how long the program will run for
    # get current directory
    print("hello!")
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
        print("running headless")
        model_num = 1
    else: 
        model_num = input("Enter model number. {models}:".format(models=model_tuples))
    model_path = current_dir+'/models/{m}'.format(m = model_tuples[int(model_num)][0])
    debug_print("Using model: {m}".format(m = model_tuples[int(model_num)][0]))
    # check if the model is an lstm
    if "lstm" in model_path:
        lstm = True
        # load the lstm model
        from keras.models import load_model
        loaded_model = load_model(model_path)
    else:
        # load the model
        loaded_model = joblib.load(model_path)
    try:
        # loop = asyncio.new_event_loop()
        if async_loop == None: # if loop is not passed in because headless is false
            async_loop = asyncio.get_event_loop()
        # get a new event loop
        tap_device = connect_to_tapstrap(async_loop,on_raw_data,run_time)
        async_loop.run_until_complete(tap_device)
        # loop.run_until_complete(run(loop, True))
    except KeyboardInterrupt:
        debug_print("KeyboardInterrupt")
        async_loop.close()
    except Exception as e:
        debug_print(e)
        async_loop.close()

if __name__ == "__main__":
    main()
    


