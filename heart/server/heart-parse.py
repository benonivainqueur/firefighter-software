import pathlib

from collections import defaultdict
from typing import List


class ActionData:
    start_time: float
    end_time: float
    duration: float
    heart_rate_measurements: dict

    def __init__(self, start_time):
        self.start_time = start_time
        self.end_time = -1
        self.heart_rate_measurements = defaultdict(lambda: 0)
        self.heart_rate_perc_measurements = defaultdict(lambda: 0)

    @property
    def duration(self):
        if self.end_time > self.start_time:
            return self.end_time - self.start_time
        return -1

    def __hash__(self):
        return hash(hash(self.start_time) + hash(self.end_time))


def index_within_range(value, value_range):
    for index in range(len(value_range)-2):
        if value_range[index] <= value < value_range[index+1]:
            return index
    return -1


data_location = pathlib.Path(__file__).parent.resolve() / "heart_data"  # change per setup
log_filename = input("Log file name to parse: ")
if not log_filename.endswith('.log'):
    log_filename = log_filename + '.log'
if 'heart_data' not in log_filename:
    log_filename = data_location / log_filename
wearer_age = None
while wearer_age is None:
    wearer_age = input("Enter wearer's age: ")
    wearer_age = int(wearer_age) if wearer_age.isdecimal() else None

estimated_max_heart_rate = 192 - (0.007*(wearer_age**2))
estimated_resting_heart_rate = 70

all_recorded_actions: List[ActionData] = []
currently_in_action = False
current_action: ActionData = None
with open(log_filename, 'r') as log_file:
    for line in log_file.readlines():
        if "|" in line:
            timestamp, data = line.strip().split("|", 1)
            if data == "START":
                if current_action is not None:
                    print(f"ISSUE WITH ACTION AT {current_action.start_time} AND NEW ACTION AT {timestamp}")
                current_action = ActionData(float(timestamp))
            elif data == "STOP":
                if current_action is None:
                    print(f"ISSUE WITH STOP CALL AT {timestamp}, NO ACTION BEFORE")
                current_action.end_time = float(timestamp)
                all_recorded_actions.append(current_action)
                current_action = None
            if data.isdecimal() and current_action is not None:
                percent_max_heart_rate = int(data) / (estimated_max_heart_rate - wearer_age)
                current_action.heart_rate_measurements[int(data)] += 1
                current_action.heart_rate_perc_measurements[percent_max_heart_rate] += 1


heart_rate_ranges = [0, .50, .70, .85, 1]
heart_rate_range_keys = [f'{low}-{high}' for low, high in zip(heart_rate_ranges[:-1], heart_rate_ranges[1:])]


parsed_log_file = log_filename.replace(".log", ".plog")
with open(parsed_log_file, 'w+') as parsed_log:
    for action in all_recorded_actions:
        action_name = input("Please name the action starting at {:.4f} and lasting {:.2f}s -> ".format(action.start_time, action.duration))

        heart_rate_ranged_dist = {key: 0 for key in heart_rate_range_keys}
        heart_rate_measurement_with_times = [(heart_rate_perc, count) for heart_rate_perc, count in action.heart_rate_measurements.items()]
        heart_rate_perc_with_times = [(heart_rate_perc, count) for heart_rate_perc, count in action.heart_rate_perc_measurements.items()]

        for heart_rate_perc, count in heart_rate_perc_with_times:
            val_index = index_within_range(heart_rate_perc, heart_rate_ranges)
            if val_index >= 0:
                range_key = heart_rate_range_keys[val_index]
                heart_rate_ranged_dist[range_key] += count

        parsed_log.write(action_name + "\n")
        parsed_log.write(str(sorted(heart_rate_measurement_with_times, key=lambda x: x[0])) + "\n")
        parsed_log.write(str(sorted(heart_rate_perc_with_times, key=lambda x: x[0])) + "\n")
        parsed_log.write(str(sorted(heart_rate_ranged_dist.items(), key=lambda x: x[0])) + "\n\n")

        print(heart_rate_ranged_dist.items())
