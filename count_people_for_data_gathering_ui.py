import csv
import tkinter as tk
from datetime import datetime
import time
import os


TIME_STAMP = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
RECORDING_NAME = input("Recording_name: ").replace(" ", "_").replace(".", "-")
FOLDER = "data_gathering"


class Count:
    def __init__(self, csv_file, backup_csv_file):
        self.csv_file = csv_file
        self.backup_csv_file = backup_csv_file
        self.first_time = None
        self.last_clicked_time = datetime.now()
        self.root = tk.Tk()

    def showNumber(self, occupancy_count):
        current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        time_in_seconds = time.time()
        if self.first_time is None:
            self.first_time = time_in_seconds
        seconds_from_start = time_in_seconds - self.first_time

        # Write CSV
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                current_time,
                round(time_in_seconds, 2),
                round(seconds_from_start, 2),
                occupancy_count,
            ])
        # Write backup CSV
        with open(self.backup_csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                current_time,
                round(time_in_seconds, 2),
                round(seconds_from_start, 2),
                occupancy_count,
            ])
        self.count_label.config(text=f"{occupancy_count}")
        self.resetTimer()

    def resetTimer(self):
        self.last_clicked_time = datetime.now()

    def update_timer(self):
        elapsed_time = datetime.now() - self.last_clicked_time
        minutes = elapsed_time.seconds // 60
        seconds = elapsed_time.seconds % 60
        if minutes >= 5:
            color = "red"
        elif minutes >= 3:
            color = "orange"
        else:
            color = None
        self.time_label.config(
            text=f"Time since last click: {minutes:02}:{seconds:02}",
            anchor="e",
            fg=color,
        )

        # Update every 100 ms
        self.root.after(100, self.update_timer)

    def initializeWindow(self):
        # Initialize the main application window
        self.root.title("Occupancy data")
        self.root.geometry("800x550")

        # Label of last click
        self.time_label = tk.Label(
            self.root, text="Time since last click: 00:00",
            font=("Arial", 15),
            anchor="e",
        )
        self.time_label.pack(pady=5, padx=20, fill="x")

        # Create a label to display the selected number
        self.count_label = tk.Label(self.root, text="None", font=("Arial", 50))
        self.count_label.pack(pady=5)

        # Break button
        button = tk.Button(
            self.root, text="Break", font=("Arial", 14), width=4, height=2,
            command=lambda count="Break": self.showNumber(count)
        )
        button.pack(pady=5)

        # Create a frame to hold the buttons in a grid layout
        frame = tk.Frame(self.root)
        frame.pack()

        # Create buttons for numbers 0 to 29
        j = 0
        for i in (
            list(range(0, 70))
            #list(range(30, 50, 2)) +
            #list(range(50, 100, 5)) +
            #list(range(100, 200, 10))
        ):
            button = tk.Button(
                frame, text=str(i), font=("Arial", 14), width=4, height=2,
                command=lambda i=i: self.showNumber(i)
            )
            # Arrange buttons in a 5x6 grid
            button.grid(row=j // 10, column=j % 10, padx=5, pady=5)
            j += 1

        # Run the application
        self.update_timer()
        self.root.mainloop()


def main():
    # CSV file
    os.makedirs(FOLDER, exist_ok=True)
    csv_file = f"{FOLDER}/{TIME_STAMP}_{RECORDING_NAME}.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Seconds", "Seconds-from-start", "Count"])
    print("File created:")
    print(csv_file)

    # Backup CSV
    backup_folder = f"{FOLDER}_backup"
    os.makedirs(backup_folder, exist_ok=True)
    backup_csv_file = f"{backup_folder}/{TIME_STAMP}_{RECORDING_NAME}.csv"
    with open(backup_csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Seconds", "Seconds-from-start", "Count"])

    occupancy_count = Count(csv_file, backup_csv_file)
    occupancy_count.initializeWindow()


main()
