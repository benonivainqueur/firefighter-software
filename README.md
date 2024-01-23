# firefighter-software
This repository implements an end-to-end pipeline for detecting hand gestures using the Tapstrap wearable device. It leverages the device's inbuilt accelerometer and IMU sensors to capture motion data associated with different gestures.

The tapstrap_gesture_recorder.py script allows collecting timestamped sensor data streams from the Tapstrap. It preprocesses and saves the data organized by gesture type.

The gesture_recognition.ipynb Jupyter notebook provides exploratory data analysis on the raw sensor data. It extracts statistical and frequency-based features from the time series data.

Multiple machine learning models are implemented and evaluated on the extracted features. The models identify characteristic patterns in the features to differentiate between gesture classes.

The realtime_inference.py script demonstrates a real-time gesture recognition pipeline. It uses a pretrained model to predict gestures as the user performs them while wearing the Tapstrap.

The tools.py module contains the core feature extraction and data preprocessing functions. This implements reusable logic that is leveraged across the pipeline.

Overall, the repository provides a template that uses Python, TapSDK and scikit-learn to build a gesture classifier on wearable sensor data. It can serve as a starting point for similar projects using the Tapstrap or other motion sensing devices.

The README within the tapstrap folder provides setup instructions, usage examples and ideas for enhancing the project further. Documentation within the code explains the implementation details.

Let me know if you need any other overview or summary of the repository! I'm happy to provide more details on specific parts as well.