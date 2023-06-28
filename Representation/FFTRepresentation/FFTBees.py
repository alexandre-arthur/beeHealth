import matplotlib.pyplot as plt
import numpy as np
import librosa as rosa
import os
import statistics as stat
from scipy import signal

PATH = 'Representation\BeeDataset\OnlyBees'

PATHS = [PATH + "\\Active", PATH + "\\MissingQueen", PATH + "\\NoQueen", PATH + "\\QueenBee"]

colors = ["m",
          "g",
          "b",
          "r"]

def notch_filter(y_pure, samp_freq, notch_freq) :
    # Create/view notch filter
    # Frequency to be removed from signal (Hz)
    quality_factor = 30.0  # Quality factor
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)

    # apply notch filter to signal
    y_notched = signal.filtfilt(b_notch, a_notch, y_pure)
    return y_notched

for i in range(4):
    highest_frequencies = []
    PATH = PATHS[i]
    FILE_NAMES = os.listdir(PATH)
    for FILE in FILE_NAMES:
        print(FILE)
        FILE_NAME = PATH + '\\' + FILE
        # Load the audio file
        data, sample_rate = rosa.load(FILE_NAME)

        # Filtering the audio signal
        CUT_OFF_FREQUENCY = 4000
        FILTER_ORDER = 8
        #sos = signal.butter(FILTER_ORDER, CUT_OFF_FREQUENCY, 'lp', fs=sample_rate, output='sos') # Window
        #filtered = signal.sosfilt(sos, data) # Filter
        #data = filtered
        data = notch_filter(data, sample_rate, 150)
        data = notch_filter(data, sample_rate, 100)
        data = notch_filter(data, sample_rate, 50)
        data = notch_filter(data, sample_rate, 49)
        data = notch_filter(data, sample_rate, 25)

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
        high_freq = abs(frequencies[argmax])
        print(high_freq)
        highest_frequencies.append(high_freq)

    x = np.arange(len(highest_frequencies))
    y = highest_frequencies
    print("moyenne : " +  str(stat.mean(highest_frequencies)))
    plt.scatter(y, x, color = colors[i], marker = "o", s = 30, label=PATH)


# putting labels
plt.xlabel('Frequency (Hz)')
plt.ylabel('Presence')
plt.title('FFT max')
plt.legend(loc="upper left")
#plt.xlim(0, len(highest_frequencies))

# function to show plot
plt.savefig(PATH + 'last_plot.png')
plt.show()