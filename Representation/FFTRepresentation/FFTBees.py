import matplotlib.pyplot as plt
import numpy as np
import librosa as rosa
import os
from scipy import signal

PATH = 'Representation\Audio\AudioLessThan2Mins'
FILE_NAMES = os.listdir(PATH)

for FILE in FILE_NAMES:
    FILE_NAME = PATH+'\\'+FILE
    # Load the audio file
    data, sample_rate = rosa.load(FILE_NAME)

    # Filtering the audio signal
    CUT_OFF_FREQUENCY = 4000
    FILTER_ORDER = 8
    sos = signal.butter(FILTER_ORDER, CUT_OFF_FREQUENCY, 'lp', fs=sample_rate, output='sos') # Window
    filtered = signal.sosfilt(sos, data) # Filter
    data = filtered

    # Convert the audio data to mono if it has multiple channels
    if len(data.shape) > 1:
        data = data.sum(axis=1) / data.shape[1]

    # Get the duration of the file
    duration = len(data)

    # Get a list with all the time stamps
    time = range(duration)

    # Apply FFT to the audio data
    fft_data = np.fft.fft(data)

    # Calculate the magnitudes of the FFT coefficients
    magnitudes = np.abs(fft_data)
    magnitudes = magnitudes / max(magnitudes)
    maxMagnitudes = np.argmax(magnitudes)

    # Generate the corresponding frequencies for the FFT coefficients
    frequencies = np.fft.fftfreq(len(magnitudes), 1 / sample_rate)
    argmax = np.array(magnitudes).argmax()
    print(round(abs(frequencies[argmax]), 1))

    plt.plot(frequencies, magnitudes, alpha=0.7, label = FILE)

plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('FFT normalisée')
plt.xlim(0, 1000)
plt.show()