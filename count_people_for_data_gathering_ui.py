import csv
import tkinter as tk
from datetime import datetime
import time

TIME_STAMP = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
RECORDING_NAME = input("Recording_name: ").replace(" ", "_")
csv_file = f"data_gathering/{TIME_STAMP}_{RECORDING_NAME}.csv"

with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Seconds", "Count"])

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
root.geometry("400x400")

# Create a label to display the selected number
label = tk.Label(root, text="None", font=("Arial", 50))
label.pack(pady=5)

# Create a frame to hold the buttons in a grid layout
frame = tk.Frame(root)
frame.pack()

# Create buttons for numbers 0 to 29
for i in range(0, 30):
    button = tk.Button(
        frame, text=str(i), font=("Arial", 14), width=4, height=2,
        command=lambda i=i: show_number(i)
    )
    # Arrange buttons in a 5x6 grid
    button.grid(row=i // 5, column=i % 5, padx=5, pady=5)

# Run the application
root.mainloop()
