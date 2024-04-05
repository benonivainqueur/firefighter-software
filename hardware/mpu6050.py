import smbus2
import time
import math

# Define I2C addresses for the sensors
MPU6050_ADDR = 0x68
GY273_ADDR = 0x0D

# Register addresses for MPU-6050
MPU6050_PWR_MGMT_1 = 0x6B
MPU6050_TEMP_OUT_H = 0x41
MPU6050_TEMP_OUT_L = 0x42
MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_ACCEL_XOUT_L = 0x3C
MPU6050_ACCEL_YOUT_H = 0x3D
MPU6050_ACCEL_YOUT_L = 0x3E
MPU6050_ACCEL_ZOUT_H = 0x3F
MPU6050_ACCEL_ZOUT_L = 0x40
MPU6050_GYRO_XOUT_H = 0x43
MPU6050_GYRO_XOUT_L = 0x44
MPU6050_GYRO_YOUT_H = 0x45
MPU6050_GYRO_YOUT_L = 0x46
MPU6050_GYRO_ZOUT_H = 0x47
MPU6050_GYRO_ZOUT_L = 0x48

# Register addresses for QMC5883L
GY273_CONTROL_REGISTER = 0x09
GY273_DATA_REGISTER = 0x00

# Create an SMBus object for communication with the I2C buses
bus = smbus2.SMBus(3)  # I2C bus 3
magneto_bus = smbus2.SMBus(0)  # I2C bus 0

# Calibration constants for magnetometer (calibrate as needed)
OFFSET_X = 0
OFFSET_Y = 0
OFFSET_Z = 0

SCALE_X = 1.0
SCALE_Y = 1.0
SCALE_Z = 1.0

# Function to read data from the MPU-6050 accelerometer
def read_mpu6050_accel_data():
    # Wake up the MPU-6050 by writing 0 to PWR_MGMT_1 register
    bus.write_byte_data(MPU6050_ADDR, MPU6050_PWR_MGMT_1, 0)
    
    # Read raw accelerometer data
    accel_x_raw = bus.read_i2c_block_data(MPU6050_ADDR, MPU6050_ACCEL_XOUT_H, 2)
    accel_y_raw = bus.read_i2c_block_data(MPU6050_ADDR, MPU6050_ACCEL_YOUT_H, 2)
    accel_z_raw = bus.read_i2c_block_data(MPU6050_ADDR, MPU6050_ACCEL_ZOUT_H, 2)
    
    # Combine high and low bytes into signed 16-bit values
    accel_x = (accel_x_raw[0] << 8) | accel_x_raw[1]
    accel_y = (accel_y_raw[0] << 8) | accel_y_raw[1]
    accel_z = (accel_z_raw[0] << 8) | accel_z_raw[1]
    
    # Return accelerometer data
    return accel_x, accel_y, accel_z

# Function to read data from the MPU-6050 gyroscope
def read_mpu6050_gyro_data():
    # Read raw gyroscope data
    gyro_x_raw = bus.read_i2c_block_data(MPU6050_ADDR, MPU6050_GYRO_XOUT_H, 2)
    gyro_y_raw = bus.read_i2c_block_data(MPU6050_ADDR, MPU6050_GYRO_YOUT_H, 2)
    gyro_z_raw = bus.read_i2c_block_data(MPU6050_ADDR, MPU6050_GYRO_ZOUT_H, 2)
    
    # Combine high and low bytes into signed 16-bit values
    gyro_x = (gyro_x_raw[0] << 8) | gyro_x_raw[1]
    gyro_y = (gyro_y_raw[0] << 8) | gyro_y_raw[1]
    gyro_z = (gyro_z_raw[0] << 8) | gyro_z_raw[1]
    
    # Return gyroscope data
    return gyro_x, gyro_y, gyro_z

# Function to read data from the MPU-6050 temperature sensor
def read_mpu6050_temp():
    # Read raw temperature data
    temp_raw = bus.read_i2c_block_data(MPU6050_ADDR, MPU6050_TEMP_OUT_H, 2)
    
    # Combine high and low bytes into signed 16-bit value
    temp = (temp_raw[0] << 8) | temp_raw[1]
    
    # Convert raw temperature data to Celsius
    temperature = (temp / 340.0) + 36.53
    
    # Return temperature
    return temperature

# Function to read data from the GY-273 magnetometer (QMC5883L)
def read_gy273_data():
    # Set the operation mode to continuous measurement mode
    magneto_bus.write_byte_data(GY273_ADDR, GY273_CONTROL_REGISTER, 0x01)

    # Wait for the measurement to complete (depends on the sensor's configuration)
    time.sleep(0.1)  # Adjust as needed

    # Read the magnetometer data registers (6 bytes for X, Y, Z axes)
    data = magneto_bus.read_i2c_block_data(GY273_ADDR, GY273_DATA_REGISTER, 6)

    # Combine the bytes to form signed 16-bit integers
    x_raw = data[0] | (data[1] << 8)
    y_raw = data[2] | (data[3] << 8)
    z_raw = data[4] | (data[5] << 8)

    # Apply calibration offsets and scaling
    x_calibrated = (x_raw - OFFSET_X) * SCALE_X
    y_calibrated = (y_raw - OFFSET_Y) * SCALE_Y
    z_calibrated = (z_raw - OFFSET_Z) * SCALE_Z

    # Calculate heading or angle
    heading = math.atan2(y_calibrated, x_calibrated) * 180 / math.pi

    # Return the calibrated magnetometer data and heading
    return x_calibrated, y_calibrated, z_calibrated, heading

# Main loop to continuously read data from both sensors
while True:
    # Read data from sensors
    accel_data = read_mpu6050_accel_data()
    # derive the current direction we are walking in 
    gyro_data = read_mpu6050_gyro_data()
    magneto_data = read_gy273_data()
    
    # Read temperature data from MPU-6050
    temp_mpu6050 = read_mpu6050_temp()

    # Print the sensor data
    print("MPU-6050 Accelerometer Data (X, Y, Z):")
    print("   X-axis: {} m/s^2".format(accel_data[0] / 16384.0))
    print("   Y-axis: {} m/s^2".format(accel_data[1] / 16384.0))
    print("   Z-axis: {} m/s^2".format(accel_data[2] / 16384.0))

    print("MPU-6050 Gyroscope Data (X, Y, Z):")
    print("   X-axis: {} degrees/s".format(gyro_data[0] / 131.0))
    print("   Y-axis: {} degrees/s".format(gyro_data[1] / 131.0))
    print("   Z-axis: {} degrees/s".format(gyro_data[2] / 131.0))

    print("MPU-6050 Temperature: {:.2f} °C".format(temp_mpu6050))

    print("GY-273 Magnetometer Data (X, Y, Z):")
    print("   X-axis: {:.2f} microteslas".format(magneto_data[0]))
    print("   Y-axis: {:.2f} microteslas".format(magneto_data[1]))
    print("   Z-axis: {:.2f} microteslas".format(magneto_data[2]))

    # Print heading calculated from magnetometer data
    print("Heading (angle with respect to magnetic north): {:.2f} degrees".format(magneto_data[3]))

    # Delay for a short period before reading again
    time.sleep(1)  # Adjust as needed