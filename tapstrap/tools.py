import pandas as pd
import json
import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.signal import find_peaks
from tabulate import tabulate
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from tabulate import tabulate


pd.set_option('display.max_columns', 200)  # max 20 columns to be displayed
pd.set_option('display.max_rows', 100)    # max 100 rows to be displayed

def feature_extraction(new_dataframe, use_label, interpolated = False, assign_label = None,normalize=False):
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

    # table(data_df)
    # print('SHAPE:', data_df.shape)
    return data_df

'''
    This function will take in a list of packets, and merge them together.
    The way it is being merged is by taking the closest imu packet to the accl packet, and merging them.
    
    input: list of packets
    output: list of merged packets
'''
def merge_packets(packets, prexisting=False, remove_label=False, collecting_data=False):
    accl_packets = [p for p in packets if p['type'] == 'accl']
    imu_packets = [p for p in packets if p['type'] == 'imu']
    merged_packets = []

    for accl_packet in accl_packets:
        closest_imu = min(imu_packets, key=lambda imu: abs(imu['ts'] - accl_packet['ts']))
        merged_payload = closest_imu['payload'] + accl_packet['payload']
        if(prexisting):
            merged_packets.append({"timestamp": accl_packet['ts'], "payload": merged_payload, "label": accl_packet['label']})
        elif(remove_label):
            merged_packets.append({"ts": accl_packet['ts'], "payload": merged_payload})
        elif(collecting_data):
            merged_packets.append({ 'ts': accl_packet['ts'], 'payload': merged_payload})
        else:
            merged_packets.append({ 'ts': accl_packet['ts'], 'payload': merged_payload, 'label': accl_packet['label']})
    return merged_packets

'''
    takes a accel file name, and imu file name, and merges them together
    '''
def merge_files(accel_file_name, imu_file_name):
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