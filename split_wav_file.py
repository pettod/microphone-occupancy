from pydub import AudioSegment
import os


FILE_NAME = "20241102_111235.WAV"
SEGMENT_DURATION_MS = 260000
OUTPUT_FOLDER = "output_segments"


def split_wav(file_path, segment_duration_ms, output_folder):
    # Load the audio file
    audio = AudioSegment.from_wav(file_path)
    
    # Calculate the number of segments
    total_duration_ms = len(audio)
    num_segments = total_duration_ms // segment_duration_ms + (1 if total_duration_ms % segment_duration_ms != 0 else 0)
    
    # Loop through and export each segment
    for i in range(num_segments):
        start = i * segment_duration_ms
        end = min((i + 1) * segment_duration_ms, total_duration_ms)
        
        # Extract the segment
        segment = audio[start:end]
        
        # Save segment as a new WAV file
        segment.export(f"{output_folder}/{FILE_NAME}-segment{i + 1}.WAV", format="wav")
        print(f"Segment {i + 1} exported from {start} ms to {end} ms")


os.makedirs(OUTPUT_FOLDER, exist_ok=True)
split_wav(FILE_NAME, segment_duration_ms=SEGMENT_DURATION_MS, output_folder=OUTPUT_FOLDER)
