import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from tabulate import tabulate

import seaborn as sns
# import joblib
# import json
import sys
import __init__
sys.path.append( sys.path[0] + "/..")

# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import accuracy_score, classification_report
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.linear_model import LogisticRegression

# pd.set_option('display.max_columns', 200)  # max 20 columns to be displayed
# pd.set_option('display.max_rows', 100)    # max 100 rows to be displayed

def on_linux():
    import platform
    if platform.system() == "Linux":
        return True
    else:
        return False

def rolling_feature_extraction(new_dataframe, use_label, interpolated = False, normalize=False,assign_label=None):
    """
    Extracts rolling features from a given dataframe.

    Parameters:
    new_dataframe (pd.DataFrame): The input dataframe.
    use_label (bool): Flag indicating whether to include the label in the output dataframe.
    interpolated (bool, optional): Flag indicating whether the dataframe contains interpolated data. Defaults to False.
    normalize (bool, optional): Flag indicating whether to normalize the data. Defaults to False.
    assign_label (int, optional): The label to assign to the output dataframe. Defaults to None.

    Returns:
    pd.DataFrame: The dataframe with rolling features extracted.
    """
    # supress warnings
    features = ['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 'middle_x', 'middle_y', 'middle_z',
                'ring_x', 'ring_y', 'ring_z', 'pinky_x', 'pinky_y', 'pinky_z']

    fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
    if interpolated:
        imu_features = ['thumb_imu_x', 'thumb_imu_y', 'thumb_imu_z', 'thumb_imu_pitch', 'thumb_imu_yaw', 'thumb_imu_roll']

        features = imu_features +  ['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 'middle_x', 'middle_y', 'middle_z',
                'ring_x', 'ring_y', 'ring_z', 'pinky_x', 'pinky_y', 'pinky_z'] 

    # Average acceleration per axis
    
    new_df = pd.DataFrame()
    new_df = new_dataframe[features]
    rolling_data_frames = []
    # print("num nans:", new_df.isnull().sum().sum())
    cols = new_df.columns.tolist()
    window_size = 15

    if normalize:
        new_dataframe[features] = new_dataframe[features].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    for feature in features:
        new_df['{}_rolling_mean'.format(feature)] = new_df[feature].rolling(window=window_size).mean()
        new_df['{}_rolling_std'.format(feature)] = new_df[feature].rolling(window=window_size).std()
        new_df['{}_rolling_variance'.format(feature)] = new_df[feature].rolling(window=window_size).var()
        new_df['{}_rolling_derivative'.format(feature)] = new_df['{}'.format(feature)].diff()
    


    if(use_label):
        new_df['label'] = new_dataframe['label'][0]  # this will either be 0 or 1
    
    if (assign_label != None ):
        new_df['label'] = assign_label
    # drop first n rows where n is the window size
    new_df = new_df[window_size:]

    # table(data_df)
    # print('SHAPE:', data_df.shape)
    return new_df



def reshape_data(data, window_size=100, use_label=False):
    """
    Reshapes the input data into sequences of a specified window size.

    Parameters:
    - data: The input data, either a pandas DataFrame or a numpy array.
    - window_size: The size of the sliding window to create sequences.
    - use_label: Whether to include labels in the output sequences.

    Returns:
    - sequences: The reshaped data as sequences.
    - labels: The labels corresponding to each sequence (if use_label is True).
    """
    sequences = []
    labels = []
    if use_label:
        for i in range(len(data) - window_size):
            sequence = data.iloc[i:i+window_size].values
            sequence = sequence[:, :-1]
            sequences.append(sequence)
            if use_label:
                labels.append(data.iloc[i+window_size][-1])

        sequences = np.array(sequences)
        labels = np.array(labels)
        return sequences, labels
    else:
        for i in range(len(data) - window_size):
            sequence = data.iloc[i:i+window_size].values
            sequences.append(sequence)
        sequences = np.array(sequences)
        labels = np.array(labels)
        return sequences


def feature_extraction(new_dataframe, use_label, interpolated = False, assign_label = None, normalize=False, speedup_multiplier = 1):
    """
    Extracts features from a given dataframe.

    Parameters:
    - new_dataframe (DataFrame): The input dataframe containing the data.
    - use_label (bool): Flag indicating whether to include the label in the output dataframe.
    - interpolated (bool): Flag indicating whether the data is interpolated.
    - assign_label (int or None): The label to assign to the output dataframe. If None, the label from the input dataframe is used.
    - normalize (bool): Flag indicating whether to normalize the values in the dataframe.
    - speedup_multiplier (int): The multiplier for speeding up the data by taking every nth row.

    Returns:
    - data_df (DataFrame): The output dataframe containing the extracted features.
    """
    features = ['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 'middle_x', 'middle_y', 'middle_z',
                'ring_x', 'ring_y', 'ring_z', 'pinky_x', 'pinky_y', 'pinky_z']

    fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
    if interpolated:
        imu_features = ['thumb_imu_x', 'thumb_imu_y', 'thumb_imu_z', 'thumb_imu_pitch', 'thumb_imu_yaw', 'thumb_imu_roll']

        features = imu_features +  ['thumb_x', 'thumb_y', 'thumb_z', 'index_x', 'index_y', 'index_z', 'middle_x', 'middle_y', 'middle_z',
                'ring_x', 'ring_y', 'ring_z', 'pinky_x', 'pinky_y', 'pinky_z'] 
    # normalize all the values
    if normalize:
        new_dataframe[features] = new_dataframe[features].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    # Average acceleration per axis
    
    # label = new_dataframe['label']
    # label_value = label[0]
    # table(new_dataframe)
    avg_accel = new_dataframe[features].mean()
    # print(avg_accel)

    # calculate the average jerk per axis
    avg_jerk = new_dataframe[features].diff().mean()

    # calculate the variance per axis
    variance = new_dataframe[features].var()
    
    # print("JERK \n", avg_jerk)

    # Standard deviation per axis
    std_dev_accel = new_dataframe[features].std()
    # print(std_dev_accel)
    skew = new_dataframe[features].skew()
    kurtosis = new_dataframe[features].kurtosis()
    # Average absolute difference per axis
    avg_abs_diff_accel = new_dataframe[features].diff().abs().mean()
    # print(avg_abs_diff_accel)

    # Initialize dictionary to hold results
    avg_accel_mag = {}
    # Loop over each finger and calculate the average acceleration magnitude
    for finger in fingers:
        avg_accel_mag[finger] = ((new_dataframe[[f'{finger}_x', f'{finger}_y', f'{finger}_z']] ** 2).sum(axis=1) ** 0.5).mean()
    # rename each key to be avg_accel_mag_{finger}
    # print(avg_accel_mag)
    # Time between peaks per axis
    time_between_peaks = {}
    for feature in features:
        peaks, _ = find_peaks(new_dataframe[feature])
        # check that there are peaks
        if len(peaks) > 1:
            time_between_peaks[feature] = np.diff(peaks).mean()
            # if np.isnan(time_between_peaks[feature]):
            #     time_between_peaks[feature] = 0
        else:
            time_between_peaks[feature] = 0
    # print(time_between_peaks)

    variance_dict = {f'variance_{k}': v for k, v in variance.items()}

    # rename each key to be avg_accel_{finger}
    avg_accel_dict = {f'avg_accel_{k}': v for k, v in avg_accel.items()}
    # print("Average acceleration\n", avg_accel_dict)
    # rename each key to be std_dev_accel_{finger}
    std_dev_accel_dict = {f'std_dev_accel_{k}': v for k, v in std_dev_accel.items()}
    # print("Accel Std Dev.\n", std_dev_accel_dict)
    # rename each key to be avg_abs_diff_accel_{finger}
    avg_abs_diff_accel_dict = {f'avg_abs_diff_accel_{k}': v for k, v in avg_abs_diff_accel.items()}
    # print("Average Accel Absolute Diff\n", avg_abs_diff_accel_dict)
    time_between_peaks_dict = {f'time_between_peaks_{k}': v for k, v in time_between_peaks.items()}
    # print("Time B/W Peaks\n", time_between_peaks_dict)
    avg_accel_mag_dict = {f'avg_accel_mag_{k}': v for k, v in avg_accel_mag.items()}
    # print("Average Accel mag\n", avg_accel_mag_dict
    avg_jerk_dict = {f'avg_jerk_{k}': v for k,v in avg_jerk.items()}
    kurtosis_dict = {f'kurtosis_{k}': v for k, v in kurtosis.items()}
    skew_dict = {f'skew_{k}': v for k, v in skew.items()}

    # Convert dictionaries to DataFrames
    avg_accel_df = pd.DataFrame(avg_accel_dict, index=[0])
    std_dev_accel_df = pd.DataFrame(std_dev_accel_dict, index=[0])
    avg_abs_diff_accel_df = pd.DataFrame(avg_abs_diff_accel_dict, index=[0])
    time_between_peaks_df = pd.DataFrame(time_between_peaks_dict, index=[0])
    # replace all NaN values with 0
    time_between_peaks_df = time_between_peaks_df.fillna(0)
    avg_accel_mag_df = pd.DataFrame(avg_accel_mag_dict, index=[0])
    avg_jerk_df = pd.DataFrame(avg_jerk_dict, index=[0])
    kurtosis_df = pd.DataFrame(kurtosis_dict, index=[0])
    skew_df = pd.DataFrame(skew_dict, index=[0])
    variance_df = pd.DataFrame(variance_dict, index=[0])

    # filter out any NaN values
    # replace all NaN values with 0
    time_between_peaks_df = time_between_peaks_df.fillna(0)
    # time_between_peaks_df = avg_accel_df.dropna(axis=1)
    # Concatenate DataFrames
    data_df = pd.concat([variance_df,skew_df,kurtosis_df,avg_accel_df, std_dev_accel_df, avg_abs_diff_accel_df, time_between_peaks_df, avg_accel_mag_df, avg_jerk_df], axis=1)
    if(use_label):
        data_df['label'] = new_dataframe['label'][0]  # this will either be 0 or 1
    if (assign_label != None ):
        data_df['label'] = assign_label

    
    if (speedup_multiplier > 1):
        # print("Speedup Multiplier: ", speedup_multiplier)
        # print("Old Shape: ", data_df.shape)
        data_df = data_df.iloc[::speedup_multiplier, :] # speed up the data by taking every nth row
        # print("New Shape: ", data_df.shape)
    # table(data_df)
    # print('SHAPE:', data_df.shape)
    return data_df

def merge_packets(packets, prexisting=False, remove_label=False, collecting_data=False):
    """
    Merge accelerometer and IMU packets based on their timestamps.

    Args:
        packets (list): List of packets containing accelerometer and IMU data.
        prexisting (bool, optional): Flag indicating whether to include the 'label' field in the merged packets. Defaults to False.
        remove_label (bool, optional): Flag indicating whether to remove the 'label' field from the merged packets. Defaults to False.
        collecting_data (bool, optional): Flag indicating whether the merged packets are being used for data collection. Defaults to False.

    Returns:
        list: List of merged packets.

    Raises:
        Exception: If an error occurs during the merging process.
    """
    # import time
    # print(packets)
    # time.sleep(1)
    accl_packets = [p for p in packets if p['type'] == 'accl']
    imu_packets = [p for p in packets if p['type'] == 'imu']
    merged_packets = []
    try:
        for accl_packet in accl_packets:
            if len(imu_packets) > 0:
                closest_imu = min(imu_packets, key=lambda imu: abs(imu['ts'] - accl_packet['ts']))
                merged_payload = closest_imu['payload'] + accl_packet['payload']
            else:
                print("No IMU Packets")
                return []
            if(prexisting):
                merged_packets.append({"timestamp": accl_packet['ts'], "payload": merged_payload, "label": accl_packet['label']})
            elif(remove_label):
                merged_packets.append({"ts": accl_packet['ts'], "payload": merged_payload})
            elif(collecting_data):
                merged_packets.append({ 'ts': accl_packet['ts'], 'payload': merged_payload})
            else:
                merged_packets.append({ 'ts': accl_packet['ts'], 'payload': merged_payload, 'label': accl_packet['label']})
        return merged_packets
    except Exception as e:
        print("Error: ", e)

'''
    takes a accel file name, and imu file name, and merges them together
    '''
def merge_files(accel_file_name, imu_file_name):
    """
    Merge accelerometer and IMU files into a single file.

    Parameters:
    accel_file_name (str): The file path of the accelerometer data file.
    imu_file_name (str): The file path of the IMU data file.

    Returns:
    None
    """
    import pandas as pd
    import numpy as np
    import json
    # load the files
    # load in the json into a list 
    json_accel = []
    json_imu = []

    with open(accel_file_name) as f:
        for line in f:
            json_accel.append(json.loads(line))
    with open(imu_file_name) as f:
        for line in f:
            json_imu.append(json.loads(line))
    
    # we can put all of the imu data, and the accel data into the a single list. 
    packets = []
    # for each item in the json accel, make the 'type' = 'accl'
    for item in json_accel:
        item['type'] = 'accl'
        # rename the "timestamp" to "ts"
        item['ts'] = item['timestamp']
        # remove the timestamp key
        # del item['timestamp']
        packets.append(item)
    # for each item in the json imu, make the 'type' = 'imu'
    for item in json_imu:
        item['type'] = 'imu'
        # rename the "timestamp" to "ts"
        item['ts'] = item['timestamp']
        # remove the timestamp key
        # del item['timestamp']
        packets.append(item)
    
    file_name = accel_file_name.replace("accel_data.json", "merged_data.json")
    merged_packets = merge_packets(packets, prexisting=True)
    
    # put the merged packets into a file named merged_packets.json
    with open(file_name, 'w') as f:
        for item in merged_packets:
            # turn the item into a string
            item = json.dumps(item)
            # replace every single quotes with double quotes
            item = item.replace("'", '"')
            f.write("%s\n" % item)

'''
this function was used to go through all the data that we already collected, and merge it. 
i am interpolating it as if i am collecitng it in real time, so when we now collect more data, it isnt 
a different format. The way it is being merged is by taking the closest imu packet to the accl packet, and merging them.
'''
def merge_preexisting_data(base_path = ''):
    base_path  = '/Users/benv/Desktop/Tap Strap/firefighter-software/tapstrap_new/training_data/data'
    import os
    import pandas as pd
    # get the folers, and iterate throug
    # print current directory
    print("cwd", os.getcwd())
    # for folder in folder
    dir_list = os.listdir(base_path)
    dir_name = base_path
    num_still_folders = len([i for i in dir_list if "Still" in i])
    num_turn_folders = len([i for i in dir_list if "Turn" in i])
    num_lever_folders = len([i for i in dir_list if "lever" in i]) 
    gesture_folders = [('Lever', num_lever_folders), ('Turn', num_turn_folders), ('Still', num_still_folders) ] # will refcator this into a simpler loop
    print("Gesture Folders: ", gesture_folders)
    acc = pd.DataFrame()
    count = 0
    # '../../data/Still2/imu_data.json'
    for gesture_name,number_items in gesture_folders:
        print('looking at ',gesture_name, "with ", number_items, "number of folders" )
        for  i in range(number_items):
            # load the data
            accel_file_name = str(f'{dir_name}/{gesture_name}{i}/accel_data.json')
            imu_file_name = str(f'{dir_name}/{gesture_name}{i}/imu_data.json')
            merge_files(accel_file_name, imu_file_name)

# Interpolating the packets again with the fixed function
# Test packets data
test_packets = [{'type': 'accl', 'ts': 5711184, 'payload': [0, 12, -29, -32, 2, -6, -32, 2, -2, -32, 0, 5, -32, 2, 3]}, 
                {'type': 'imu', 'ts': 5711185, 'payload': [-246, -119, -1, 419, 3425, -7700]}, 
                {'type': 'imu', 'ts': 5711190, 'payload': [-217, -52, 36, 421, 3432, -7715]}, 
                {'type': 'accl', 'ts': 5711193, 'payload': [0, 11, -29, -32, 2, -7, -32, 2, -2, -32, 0, 6, -32, 2, 4]}, 
                {'type': 'imu', 'ts': 5711194, 'payload': [-187, 24, 75, 421, 3440, -7683]}, 
                {'type': 'imu', 'ts': 5711199, 'payload': [-157, 91, 112, 438, 3430, -7695]}, 
                {'type': 'accl', 'ts': 5711200, 'payload': [0, 11, -29, -32, 2, -7, -32, 2, -2, -32, 0, 5, -32, 1, 4]}]

# interpolate_preexisting_data()


async def connect_to_tapstrap(loop,callback,timeout=100):
    """
    Connects to the Tap Strap device and sets up the necessary configurations.

    Parameters:
    - loop: The event loop to use for asynchronous operations.
    - callback: The callback function to handle raw data events from the Tap Strap.
    - timeout: The timeout duration in seconds for keeping the program running.

    Returns:
    None
    """
    from tapsdk import TapSDK, TapInputMode
    from tapsdk.models import AirGestures
    import asyncio
    import logging 
    from bleak import _logger as logger
    import sys
    if not on_linux():
        # from tapsdk import TapLinuxSDK
        print("Connecting to Tap Strap")
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.INFO)
        l.addHandler(h)
        logger.addHandler(h)

        tap_client = TapSDK(loop)
        devices = await tap_client.list_connected_taps()
        # print("devices",devices)
        x = await tap_client.manager.connect_retrieved()
        x = await tap_client.manager.is_connected()
        print("Connected: {}".format(x))
        await tap_client.set_input_mode(TapInputMode("raw", sensitivity=[0,0,0]))
        await tap_client.register_raw_data_events(callback)
        await tap_client.send_vibration_sequence([100,100,100])
        await asyncio.sleep(timeout, True) # this line  is to keep the program running for 50 seconds
    else: 
        print("On Linux")
        
        loop.set_debug(False)
        #l = logging.getLogger("asyncio")
        #l.setLevel(logging.DEBUG)
        # h = logging.StreamHandler(sys.stdout)
        # h.setLevel(logging.WARNING)
        #l.addHandler(h)
        # logger.addHandler(h)
        
        tap_client = TapSDK(None,loop)
        if not await tap_client.client.connect_retrieved():
            print("failed to connect to the device.")
            logger.error("failed to connect to the device.")
            return
        #x = await client.manager.connect_retrieved()
        #x = await client.manager.is_connected()
        #logger.info("Connected: {0}".format(x))
        print("Connected to {}".format(tap_client.client.address))
        logger.info("Connected to {}".format(tap_client.client.address))
        await tap_client.set_input_mode(TapInputMode("controller"))
        await tap_client.register_raw_data_events(callback)
        await tap_client.set_input_mode(TapInputMode("raw"))
        await tap_client.send_vibration_sequence([300,100,300])
        await asyncio.sleep(timeout, True) 
        


if __name__ == "__main__":
    pass

''' 
    this function will use tabulate to print out a table
    input: dataframe
    output: table
'''
def table(t) :
    table = tabulate(t, headers='keys', tablefmt='fancy_grid')
    print(table)