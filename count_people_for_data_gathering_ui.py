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
        self.label.config(text=f"{occupancy_count}")

    def initializeWindow(self):
        # Initialize the main application window
        root = tk.Tk()
        root.title("Occupancy data")
        root.geometry("800x520")

        # Create a label to display the selected number
        self.label = tk.Label(root, text="None", font=("Arial", 50))
        self.label.pack(pady=5)

        # Create a frame to hold the buttons in a grid layout
        frame = tk.Frame(root)
        frame.pack()

        # Create buttons for numbers 0 to 29
        j = 0
        for i in (
            list(range(0, 80))
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
        root.mainloop()


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
