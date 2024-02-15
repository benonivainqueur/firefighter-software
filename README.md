# firefighter-software
This repository implements an end-to-end pipeline for detecting hand gestures using the Tapstrap wearable device. It leverages the device's inbuilt accelerometer and IMU sensors to capture motion data associated with different gestures.

## Tapstrap 
The tapstrap_gesture_recorder.py script allows collecting timestamped sensor data streams from the Tapstrap. It preprocesses and saves the data organized by gesture type.

The gesture_recognition.ipynb Jupyter notebook provides exploratory data analysis on the raw sensor data. It extracts statistical and frequency-based features from the time series data.

Multiple machine learning models are implemented and evaluated on the extracted features. The models identify characteristic patterns in the features to differentiate between gesture classes.

The realtime_inference.py script demonstrates a real-time gesture recognition pipeline. It uses a pretrained model to predict gestures as the user performs them while wearing the Tapstrap. You are able to select the model at runtime.

The tools.py module contains the core feature extraction and data preprocessing functions. This implements reusable logic that is used-- mostly feature extraction.

Overall, the repository provides a template that uses Python, TapSDK and scikit-learn to build a gesture classifier on wearable sensor data. It can serve as a starting point for similar projects using the Tapstrap or other motion sensing devices.

The README within the tapstrap folder provides setup instructions, usage examples and ideas for enhancing the project further. Documentation within the code explains the implementation details.


## Heart
Legacy folder. todo. 

## Communication 
This folder is our networking investigations, i.e. sending data around. Will investigate creating a distributed lightweight server. 

Let me know if you need any other overview or summary of the repository! I'm happy to provide more details on specific parts as well.


## Hardware
OrangePi Setup
ssh root@192.168.0.63
ssh orangepi@192.168.0.63
wiki:
http://www.orangepi.org/orangepiwiki/index.php/Orange_Pi_Zero_2W#SSH_remote_login_development_board
wifi tool:
nmcli dev wifi
sudo nmcli dev wifi connect wifi_name password wifi_passwd
bluetooth tool:
bluetoothctl
Method to create WIFI hotspot through create_ap

http://www.orangepi.org/orangepiwiki/index.php/Orange_Pi_Zero_2W#SSH_remote_login_development_board
https://github.com/oblique/create_ap


## Networking Links
https://github.com/waterrmalann/NetworkBandwidthMonitor
https://github.com/Goldent00thbrush/Bandwidth_Monitor
https://openthread.io/guides/thread-primer
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7899530
https://ieeexplore.ieee.org/document/8421863
https://ieeexplore.ieee.org/document/8650222
https://ieeexplore.ieee.org/document/6132771
https://ieeexplore.ieee.org/document/7873617
https://ieeexplore.ieee.org/document/5633776
https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=BATMAN

BATMAN NS3 sim:https://www.youtube.com/watch?v=wZMTW7vw05Q&ab_channel=NS3simulations


- Benoni Vainqueur 