import numpy as np
import csv
import time
import glob

FINGERS = ["thumb", "index", "middle", "ring", "pinky"]
AXES = ["x", "y", "z"]


def finger_ax_iter():
    for f in [0, 1, 2, 3, 4]:
        for a in [0, 1, 2]:
            yield f, a

# Hand: T=right, F=left
# Label: T=door, F=not door
csv_fields = (
    ["filename", "hand"] +
    [f"acc_avg_{FINGERS[finger]}_{AXES[ax]}" for finger, ax in finger_ax_iter()] +
    [f"acc_std_{FINGERS[finger]}_{AXES[ax]}" for finger, ax in finger_ax_iter()] +
    [f"avg_abs_diff_{FINGERS[finger]}_{AXES[ax]}" for finger, ax in finger_ax_iter()] +
    [f"avg_mag_{FINGERS[finger]}" for finger in [0, 1, 2, 3, 4]] +
    [f"avg_t_between_peaks_{FINGERS[finger]}_{AXES[ax]}" for finger, ax in finger_ax_iter()] +
    [f"avg_gyro_{AXES[ax]}" for ax in [0, 1, 2]] +
    # binned dist here
    ["label"]
)


def find_average_time_between_peaks(raw_lines):
    hand_accel_data = [[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []]]
    for line in raw_lines:
        timestamp, data = line.split('|')
        timestamp = eval(timestamp)
        data = eval(data)
        for finger, ax in finger_ax_iter():
            hand_accel_data[finger][ax].append((timestamp, data[finger][ax]))

    time_between_peaks = [[-1] * 3] * 5
    for finger, ax in finger_ax_iter():
        hand_accel_data[finger][ax].sort(reverse=True, key=lambda x: x[1])
        time_between_peaks[finger][ax] = _find_average_time_between_peaks(hand_accel_data[finger][ax])
    return time_between_peaks


def _find_average_time_between_peaks(sorted_data, thresholds=[0.01, 0.03, 0.05, 0.10, 0.15]):
    max_sample = sorted_data[0]
    samples = sorted_data[1:]
    peaks = [max_sample]

    diff_to_beat = max_sample[1] * thresholds[0]
    #     print(f"diff to beat: {diff_to_beat}")
    for s in samples:
        if (max_sample[1] - s[1]) <= diff_to_beat:
            peaks.append(s)
        else:
            break
    if len(peaks) < 3:
        #         print(f"did not find enough peaks, recurring with threshold {thresholds[1]}")
        if len(thresholds) == 1:
            return -1
        return _find_average_time_between_peaks(sorted_data, thresholds[1:])

    peaks.sort(key=lambda s: s[0])  # sort by timestamp
    peak_gaps = [p2[0] - p1[0] for p1, p2 in zip(peaks[:-1], peaks[1:])]
    #     print(f"{len(peaks)} peaks found: {peaks}")
    #     print(f"gaps: {peak_gaps}")
    return np.mean(peak_gaps)


def create_csv_from_files(filenames, csv_name=None):
    if csv_name is None:
        csv_name = f"exported_csv_{int(time.time() * 1000)}"
    if not csv_name.endswith(".csv"):
        csv_name = csv_name + ".csv"
    print("writing csv to " + csv_name)

    with open(csv_name, "w+", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_fields)
        for file in filenames:
            # These arrays will help store in a few vars as possible
            # avg_acc[thumb,pointer,middle,ring,pinky][x,y,z] for a specific value
            avg_acc = [[-1]*3]*5
            std_dev = [[-1]*3]*5
            avg_abs_diff = [[-1]*3]*5
            avg_mag = [-1]*5
            avg_gyro = [-1]*3
            with open(file, "r") as f:
                all_lines = f.readlines()
                data_lines = [np.array(eval(line.split("|")[-1])) for line in all_lines]
                data = np.array(data_lines)
                print(f"Loaded in data of shape: {data.shape}")
                for finger in [0, 1, 2, 3, 4]:
                    avg_mag[finger] = np.mean([np.linalg.norm(val[finger]) for val in data])
                    for ax in [0, 1, 2]:
                        finger_ax_data = np.array([val[finger][ax] for val in data])
                        avg_acc[finger][ax] = np.mean(finger_ax_data)
                        std_dev[finger][ax] = np.std(finger_ax_data)
                        avg_abs_diff[finger][ax] = np.mean(np.absolute(finger_ax_data - avg_acc[finger][ax]))
                avg_time_between_peaks = find_average_time_between_peaks(all_lines)
                for ax in [0, 1, 2]:
                    avg_gyro[ax] = np.mean([val[-1][ax] for val in data if len(val) > 5])

                filename = file.split('\\')[-1]
                writer.writerow(
                    [filename, filename[0] == 'R'] +
                    [avg_acc[finger][ax] for finger, ax in finger_ax_iter()] +
                    [std_dev[finger][ax] for finger, ax in finger_ax_iter()] +
                    [avg_abs_diff[finger][ax] for finger, ax in finger_ax_iter()] +
                    [avg_mag[finger] for finger in [0, 1, 2, 3, 4]] +
                    [avg_time_between_peaks[finger][ax] for finger, ax in finger_ax_iter()] +
                    [avg_gyro[ax] for ax in [0, 1, 2]] +
                    ["door" in filename]
                )
                print(f"parse {filename}")


# create_csv_from_files(glob.glob("../raw_train_data/[L,R]*"), "firstSet")
