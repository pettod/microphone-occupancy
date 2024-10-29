from datetime import datetime
import time
import csv
import keyboard


TIME_STAMP = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
csv_file = f"data_gathering/{TIME_STAMP}.csv"

count_dict = {
    29: 0,
    18: 1,
    19: 2,
    20: 3,
    21: 4,
    23: 5,
    22: 6,
    26: 7,
    28: 8,
    25: 9,
}

with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Seconds", "Count"])

while True:
    key = keyboard.read_key(True)
    if key == "esc":
        break
    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    time_in_seconds = time.time()
    if key in count_dict:
        count = count_dict[key]
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([current_time, time_in_seconds, count])
        print(f"\n{count} at {current_time}")
    else:
        print(key, "is not in count dict")
    time.sleep(0.1)