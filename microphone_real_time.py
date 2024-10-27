import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
from collections import deque

# Audio stream parameters
AUDIO_FORMAT = pyaudio.paInt16  # Audio format (16-bit integer)
AUDIO_CHANNELS = 1              # Number of audio channels (mono)
SAMPLING_RATE = 44100           # Sampling rate (44.1 kHz)
AUDIO_BUFFER = 1024              # Size of audio buffer (frames per buffer)

# Initialize PyAudio object
p = pyaudio.PyAudio()

# Open audio stream from the microphone
stream = p.open(
    format=AUDIO_FORMAT,
    channels=AUDIO_CHANNELS,
    rate=SAMPLING_RATE,
    input=True,
    frames_per_buffer=AUDIO_BUFFER,
)

# Create a matplotlib figure with 2 subplots (one for time-domain, one for frequency-domain)
fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[:, 1])

# Create an array for the x-axis of the time-domain plot (time samples)
x_time = np.arange(0, AUDIO_BUFFER)

# Create an initial empty line for the time-domain plot
line_time, = ax1.plot(x_time, np.zeros(AUDIO_BUFFER))

# Set the y-axis limits for time-domain plot to 16-bit PCM range
ax1.set_ylim(-3000, 3000)
ax1.set_xlim(0, AUDIO_BUFFER)
ax1.set_title("Time Domain")
ax1.set_xlabel("Samples")
ax1.set_ylabel("Amplitude")

# Create an array for the x-axis of the frequency-domain plot (frequency bins)
x_freq = np.fft.fftfreq(AUDIO_BUFFER, 1/SAMPLING_RATE)[:AUDIO_BUFFER//2]  # Frequency axis (only positive frequencies)

# Create an initial empty line for the frequency-domain plot
line_freq, = ax2.plot(x_freq, np.zeros(AUDIO_BUFFER//2))

# Set the y-axis to log scale for the frequency-domain plot (FFT magnitude)
ax2.set_yscale("log")

# Set plot titles and labels for frequency domain
ax2.set_xlim(20, SAMPLING_RATE//2)  # Frequency range from 20 Hz to Nyquist frequency (SAMPLING_RATE/2)
ax2.set_ylim(0, 100000)  # Adjust based on your signal strength
ax2.set_title("Frequency Domain")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")

# Set occupancy
ax3.set_title("Occupancy")
occupancy_count_text = ax3.text(0.5, 0.5, "", fontsize=200, ha="center", va="center")
ax3.axis("off")
occupancy_filter = deque(maxlen=5)

def addElementAndGetMedian(queue, element):
    queue.append(element)
    sorted_queue = sorted(queue)
    return 1 if np.mean(sorted_queue) > 0.3 else 0

# Function to apply a moving average filter to the frequency-domain data
def moving_average(data, window_size=5):
    return np.convolve(data, np.ones(window_size)/window_size, mode="same")

# Function to update the plot with new audio data in real-time
def update_plots(frame):
    # Read AUDIO_BUFFER-size data from the audio stream and convert it to a NumPy array (time-domain data)
    data = np.frombuffer(stream.read(AUDIO_BUFFER, exception_on_overflow=False), dtype=np.int16)
    
    # Update the time-domain line data
    line_time.set_ydata(data)
    
    # Compute the FFT of the audio data and take the absolute magnitude
    fft_data = np.abs(np.fft.fft(data))[:AUDIO_BUFFER//2]  # Keep only the positive frequencies
    
    # Apply the moving average filter to smooth the frequency-domain data
    fft_data += 1
    fft_data_smoothed = moving_average(fft_data, window_size=9)
    
    # Update the frequency-domain line data with the smoothed data
    line_freq.set_ydata(fft_data_smoothed)
    occupancy_count = 1 if np.mean(np.std(data)) > 20 else 0
    occupancy_count = addElementAndGetMedian(occupancy_filter, occupancy_count)
    occupancy_count_text.set_text(occupancy_count)
    
    return line_time, line_freq, occupancy_count_text

# Create a real-time animation using FuncAnimation
ani = FuncAnimation(fig, update_plots, blit=True, interval=30)

# Show the plot in a blocking way so it keeps updating in real-time
plt.tight_layout()
plt.show()

# Stop and close the audio stream when done
stream.stop_stream()
stream.close()
p.terminate()
