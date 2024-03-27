import tensorflow as tf 

# print tensorflow version
print(tf.__version__)
# list devices
print(tf.config.list_physical_devices('GPU'))
print(tf.config.list_physical_devices('CPU'))
# Create a constant op
