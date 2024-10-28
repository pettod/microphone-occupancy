import numpy as np
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import signal

# Audio parameters
fs = 44100          # Sampling frequency
chunk = 1024        # Number of audio samples per frame
NFFT = 1024         # Length of the FFT window
noverlap = 512      # Overlap between segments
duration = 10       # Duration of audio to display (in seconds)
buffer_size = fs * duration  # Total samples to keep in buffer

# Initialize a buffer to store the audio data
audio_buffer = np.zeros(buffer_size)

# Set up the figure for plotting
fig, ax = plt.subplots(figsize=(10, 6))
Pxx, freqs, bins, im = ax.specgram(audio_buffer, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap="rainbow")
ax.set_ylim(0, fs // 2)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Live Microphone Spectrogram")
cbar = plt.colorbar(im, ax=ax)
cbar.set_label("Intensity (dB)")

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the audio stream
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=fs,
                input=True,
                frames_per_buffer=chunk)

# Callback function to update the audio buffer with new data
def update_audio_buffer():
    global audio_buffer
    # Read data from the stream
    data = stream.read(chunk, exception_on_overflow=False)
    # Convert data to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Roll buffer to the left and add new audio data to the end
    audio_buffer = np.roll(audio_buffer, chunk)
    audio_buffer[-chunk:] = audio_data

# Update function for animation
def update_spectrogram(frame):
    # Update the audio buffer with new data from the microphone
    update_audio_buffer()
    # Clear and update the spectrogram plot
    ax.clear()
    Pxx, freqs, bins, im = ax.specgram(audio_buffer, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap="rainbow")
    ax.set_ylim(0, fs // 2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Spectrogram")

# Set up the animation
ani = FuncAnimation(fig, update_spectrogram, interval=50)

plt.tight_layout()
plt.show()

# Clean up the stream and PyAudio when done
stream.stop_stream()
stream.close()
p.terminate()
