import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
from collections import deque


# Audio stream parameters
AUDIO_FORMAT = pyaudio.paInt16  # 16-bit integer
AUDIO_CHANNELS = 1              # Mono
SAMPLING_RATE = 44100
AUDIO_BUFFER = 1024             # Frames per buffer
SMOOTH_FFT = False


# Open audio stream from the microphone
p = pyaudio.PyAudio()
stream = p.open(
    format=AUDIO_FORMAT,
    channels=AUDIO_CHANNELS,
    rate=SAMPLING_RATE,
    input=True,
    frames_per_buffer=AUDIO_BUFFER,
)
is_paused = False

# Figure and axes
fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[:, 1])

# x1-axis time data and time-domain plot
x_time = np.arange(0, AUDIO_BUFFER)
plot_time_data, = ax1.plot(x_time, np.zeros(AUDIO_BUFFER))

# ax1 plot
ax1.set_ylim(-3000, 3000)
ax1.set_xlim(0, AUDIO_BUFFER)
ax1.set_title("Time Domain")
ax1.set_xlabel("Samples")
ax1.set_ylabel("Amplitude")
ax2.set_yscale("log")

# x2-axis frequency-domain data and plot
x_freq = np.fft.fftfreq(AUDIO_BUFFER, 1/SAMPLING_RATE)[:AUDIO_BUFFER//2]  # Only positive frequencies
plot_frequency_data, = ax2.plot(x_freq, np.zeros(AUDIO_BUFFER//2))

# ax2 plot
ax2.set_xlim(20, SAMPLING_RATE//2)  # Nyquist frequency (SAMPLING_RATE/2)
ax2.set_ylim(0, 10**6)
ax2.set_title("Frequency Domain")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")

# ax3 plot
ax3.set_title("Occupancy")
ax3.axis("off")

# Set occupancy
plot_occupancy_count = ax3.text(0.5, 0.5, "", fontsize=200, ha="center", va="center")
occupancy_time_window = deque(maxlen=5)

def addElementAndGetMedian(queue, element):
    queue.append(element)
    sorted_queue = sorted(queue)
    return 1 if np.mean(sorted_queue) > 0.3 else 0

def moving_average(data, window_size=5):
    return np.convolve(data, np.ones(window_size)/window_size, mode="same")

def update_plots(frame):
    # Read AUDIO_BUFFER-size data
    data = np.frombuffer(stream.read(AUDIO_BUFFER, exception_on_overflow=False), dtype=np.int16)
    plot_time_data.set_ydata(data)
    
    # FFT
    fft_data = np.abs(np.fft.fft(data))[:AUDIO_BUFFER//2]
    fft_data += 1
    if SMOOTH_FFT:
        fft_data = moving_average(fft_data, window_size=9)
    plot_frequency_data.set_ydata(fft_data)
    
    # Occupancy
    occupancy_count = 1 if np.mean(np.std(data)) > 20 else 0
    occupancy_count = addElementAndGetMedian(occupancy_time_window, occupancy_count)
    plot_occupancy_count.set_text(occupancy_count)
    
    return plot_time_data, plot_frequency_data, plot_occupancy_count

def pauseAnimation(event):
    global is_paused
    if event.key == " ":  # Check if the space bar was pressed
        if is_paused:
            animation.event_source.start()  # Resume the animation
        else:
            animation.event_source.stop()   # Pause the animation
        is_paused = not is_paused

# Pause/Resume playing
fig.canvas.mpl_connect("key_press_event", pauseAnimation)

# Update plot
animation = FuncAnimation(fig, update_plots, blit=True, interval=30)

# Plot
plt.tight_layout()
plt.show()

# Close the audio stream
stream.stop_stream()
stream.close()
p.terminate()
