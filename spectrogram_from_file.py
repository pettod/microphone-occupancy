import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys

# Load the audio file
file_path = sys.argv[1]
y, sr = librosa.load(file_path, sr=None)

# Create the spectrogram
plt.figure(figsize=(12, 8))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log') #, vmin=-80, vmax=-70)
plt.colorbar(format='%+2.0f dB')
plt.title(file_path)
plt.show()
