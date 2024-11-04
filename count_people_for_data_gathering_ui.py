import csv
import tkinter as tk
from datetime import datetime
import time
import os

TIME_STAMP = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
RECORDING_NAME = input("Recording_name: ").replace(" ", "_")
FOLDER = "data_gathering"
os.makedirs(FOLDER, exist_ok=True)
csv_file = f"{FOLDER}/{TIME_STAMP}_{RECORDING_NAME}.csv"

with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Seconds", "Count"])
print("File created:")
print(csv_file)

def show_number(number):
    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    time_in_seconds = time.time()
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([current_time, time_in_seconds, number])
    label.config(text=f"{number}")

# Initialize the main application window
root = tk.Tk()
root.title("Occupancy data")
root.geometry("800x400")

# Create a label to display the selected number
label = tk.Label(root, text="None", font=("Arial", 50))
label.pack(pady=5)

# Create a frame to hold the buttons in a grid layout
frame = tk.Frame(root)
frame.pack()

# Create buttons for numbers 0 to 29
j = 0
for i in (
    list(range(0, 30)) +
    list(range(30, 50, 2)) +
    list(range(50, 100, 5)) +
    list(range(100, 200, 10))
):
    button = tk.Button(
        frame, text=str(i), font=("Arial", 14), width=4, height=2,
        command=lambda i=i: show_number(i)
    )
    # Arrange buttons in a 5x6 grid
    button.grid(row=j // 10, column=j % 10, padx=5, pady=5)
    j += 1

# Run the application
root.mainloop()
