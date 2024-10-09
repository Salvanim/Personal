import numpy as np
from scipy.io.wavfile import write
import os

# Constants
SAMPLING_RATE = 44100  # 44.1 kHz, standard for human hearing
BIT_DEPTH = 16  # 16-bit PCM
MIN_FREQ = 20  # Minimum frequency (20 Hz)
MAX_FREQ = 20000  # Maximum frequency (20 kHz)
DURATION = 1  # Duration of each tone in seconds
OUTPUT_FILE = 'Created\combined_audio.wav'  # Output file name for the large audio

# Function to generate a sine wave at a given frequency
def generate_sine_wave(frequency, duration, sampling_rate):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * frequency * t)

# Initialize an empty list to hold the audio signals
combined_audio = []

# Generate audio for various frequencies and add them to the combined audio
for freq in range(MIN_FREQ, MAX_FREQ + 1, 1):  # Generate for every 1000 Hz step
    # Generate sine wave for this frequency
    audio_signal = generate_sine_wave(freq, DURATION, SAMPLING_RATE)
    print(audio_signal)
    # Normalize the signal to 16-bit PCM
    audio_signal = np.int16(audio_signal * 32767)

    # Append the generated signal to the combined audio list
    combined_audio.append(audio_signal)

# Convert the list of arrays into a single numpy array
combined_audio = np.concatenate(combined_audio)

# Write the combined audio to a single WAV file
write(OUTPUT_FILE, SAMPLING_RATE, combined_audio)
print(f'Generated combined audio file: {OUTPUT_FILE}')
