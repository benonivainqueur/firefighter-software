import multiprocessing
import time
import numpy as np

def generate_events(shared_data):
    while True:
        timestamp = time.time()
        # Generate some sample data
        event_data = np.random.rand(3, 3)
        
        # Write timestamped events to shared memory
        with shared_data.get_lock():
            shared_data[:3, :] = timestamp
            shared_data[3:, :] = event_data.flatten()

        time.sleep(1)  # Simulate events occurring every second

if __name__ == "__main__":
    # Define shared memory for timestamped events
    shared_data = multiprocessing.Array('d', 12)  # 3 timestamps + 9 data points

    # Create a process for generating events
    event_process = multiprocessing.Process(target=generate_events, args=(shared_data,))
    event_process.start()

    try:
        # Keep the sender process running
        event_process.join()
    except KeyboardInterrupt:
        # Terminate the process if KeyboardInterrupt (Ctrl+C) is detected
        event_process.terminate()
        event_process.join()
