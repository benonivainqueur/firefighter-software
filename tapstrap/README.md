# Tapstrap Gesture Recognition

This project focuses on recognizing hand gestures using the Tapstrap wearable device. The Tapstrap contains multiple accelerometers and an IMU sensor to capture motion data.

https://github.com/TapWithUs/tap-python-sdk

## Data Collection

The `tapstrap_gesture_recorder.py` script allows collecting timestamped accelerometer and IMU data for different gestures like turn, still, lever etc. It saves the data into separate JSON files for IMU and accelerometer. It also interpolates the accelerometer and IMU data to a common timeframe so they can be merged easily. The merged data with interpolated timestamps is also saved. 

The data is saved into incrementally numbered folders for each gesture type. This allows collecting multiple samples per gesture smoothly.

- It uses the TapSDK Python library to connect and receive data from the Tapstrap over BLE.

- Callback functions are registered to receive raw sensor data packets. 

- The data packets contain accelerometer values from 5 sensors and IMU values from the inbuilt IMU. They are timestamped to mark when they were captured.

- The script separates the stream of packets into JSON files for IMU and accelerometer data. 

- It also interpolates the 2 data streams to a common timeline since accelerometer and IMU have different sampling rates. 

- The interpolated data with merged accelerometer and IMU packets is saved to a 3rd JSON file.

- The data is saved incrementally in numbered folders for each gesture type like "Turn1", "Turn2" etc. This makes it easy to collect multiple examples of each gesture.

Overall, this provides a robust data collection pipeline to gather sensor data paired with the gesture label.

## Data Loading and Exploration

The `gesture_recognition.ipynb` Jupyter notebook shows how to load and explore the collected raw data.

- It reads the JSON files into Pandas DataFrames. 

- The sensor payload is expanded into separate columns for each axis of each sensor.

- Basic statistics like mean and standard deviation are calculated on the sensor data.

- 3D scatter plots are generated to visualize the accelerometer data.

- Detailed line plots show the time series sensor data for each axis.

- Similar exploration is done on both raw accelerometer data and the interpolated merged data.

This helps analyze the characteristics of the data and ensures the preprocessing has merged the data properly.

The various plots and statistical measures help better understand the raw sensor data before feature extraction.

## Feature Extraction

The `tools.py` module contains the main feature extraction logic.

- It extracts statistical and frequency-based features from the accelerometer and IMU data. 

- Features like mean, standard deviation, average magnitude, jerk, peaks etc. are extracted for each sensor axis.

- This consolidates the multi-axial time series data into useful summary features.

- The same module can work on just accelerometer data or the merged interpolated data.

- It returns a Pandas DataFrame containing all the feature columns ready for ML model training.

The computed features help represent the salient aspects of the sensor data that can be used to differentiate gestures.

## Model Training 

The Jupyter notebook trains various ML models on the extracted features:

- Models like Random Forest, SVM, KNN, Logistic Regression are evaluated.

- Scikit-learn is used for model implementation, training and evaluation.

- The latest model is persisted using joblib to be loaded later for inference.

- Performance metrics include accuracy, confusion matrix, classification reports etc. 

- For random forest, a feature importance analysis is provided.

- Different models provide different insights into the learned patterns in the data.

Multiple models are tested because their performance can vary significantly on different datasets.

## Real-time Inference

The `realtime_inference.py` script demonstrates a real-time inference pipeline.

- It uses the TapSDK to connect to a Tapstrap device and register callback functions.

- In the callback, it collects streaming data into a window buffer.

- Features are extracted on the windowed data and passed to the loaded model.

- The model predicts the gesture type based on the extracted features.

- This prediction is done in real-time as the user is performing the gesture.

The script shows how the trained model can be integrated with the Tapstrap to create a smart gesture controller.

## Next Steps

Some ways this project can be improved:

- Use TapSDK tools to optimize data collection with auto-labeling.

- Explore deep learning models like CNNs and LSTM RNNs that can work on raw sensor data.

- Implement the real-time inference on the jetson nano. 

- Build a mobile app interface for smart control using the predicted gestures.


# Running The Code

Install the required packages: `pip install -r deps.txt`

## Data Collection

To collect gesture data from the Tapstrap, run: `python tapstrap_gesture_recorder.py`
Follow the prompts to record different gestures. The data will be saved to training_data/ folder.

## Model Training

Open the Jupyter notebook `gesture_recognition.ipynb`
Run the cells in the notebook to load data, extract features, train models and evaluate results.

## Real-time Inference

To run real-time inference: `python realtime_inference.py`
This will load a pretrained model and display predictions as you perform gestures with the Tapstrap.
There are additional configuration options in the scripts to customize parameters. 
