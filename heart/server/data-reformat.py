import csv
import glob

log_files = glob.glob("heart_data/staircase*.log")

for log_f in log_files:
    with open(log_f, 'r') as log_file, open(log_f.replace(".log", ".csv"), 'w+', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(["timestamp", "heart"])
        for line in log_file.readlines():
            if "|" in line:
                timestamp, data = line.strip().split("|", 1)
                if data.isdecimal() or data.startswith("a+"):
                    if data.startswith("a+"):
                        data = data.replace("a+", "")
                    writer.writerow([timestamp, data])