import matplotlib.pyplot as plt
import numpy as np
import librosa as rosa
import os
import statistics as stat
import Filters as Filters

# Caculate the FFT of a wav file in a given path and filter out the some frequencies
def calculFFTFiltered(PATH, freq_filter : list | int = None, maxFrequency : int = None, verbose = False) -> list :
    highest_frequencies = []
    FILE_NAMES = os.listdir(PATH)
    for FILE in FILE_NAMES:
        FILE_NAME = PATH + '\\' + FILE
        frequencies, magnitudes = CalculFFT_File(FILE_NAME, freq_filter, maxFrequency)

        # Search the maximum
        argmax = np.array(magnitudes).argmax()
        high_freq = abs(frequencies[argmax])
        highest_frequencies.append(high_freq)
        if verbose :
            if freq_filter != None:
                print("For {Path} without {notch_freq}, we found the highest frequency at {highest_f}".format(Path = PATH, notch_freq = freq_filter, highest_f =high_freq))
            else:
                print("For {Path}, we found the highest frequency at {highest_f}".format(Path = PATH, highest_f =high_freq))
    return highest_frequencies

def CalculFFT_File(FILE_NAME, freq_filter : list | int = None, maxFrequency : int = None):
    # Load the audio file
        data, sample_rate = rosa.load(FILE_NAME)

        # Filtering the audio signal
        data = Filters.sounddata_filter(data, sample_rate, maxFrequency=maxFrequency, freq_filter=freq_filter)

        # Convert the audio data to mono if it has multiple channels
        if len(data.shape) > 1:
            data = data.sum(axis=1) / data.shape[1]

        # Apply FFT to the audio data
        fft_data = np.fft.fft(data)

        # Calculate the magnitudes of the FFT coefficients
        magnitudes = np.abs(fft_data)
        magnitudes = magnitudes / max(magnitudes)

        # Generate the corresponding frequencies for the FFT coefficients
        frequencies = np.fft.fftfreq(len(magnitudes), 1 / sample_rate)

        return frequencies, magnitudes

if __name__ == "__main__" :
    PATH = 'Representation\BeeDataset\OnlyBees'
    PATHS = [PATH + "\\Active", PATH + "\\MissingQueen", PATH + "\\NoQueen", PATH + "\\QueenBee"]

    colors = ["m", "g", "b", "r"] 
    for i in range(4):
        PATH = PATHS[i]
        highest_frequencies =  calculFFTFiltered(PATH, maxFrequency=4000, freq_filter=[150, 100, 50, 49, 25],  verbose=True)
        x = np.arange(len(highest_frequencies))
        y = highest_frequencies
        print("moyenne : " +  str(stat.mean(highest_frequencies)))
        plt.scatter(x=x, y=y, color = colors[i], marker = "o", s=30, label=PATH)

    # putting labels
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Presence')
    plt.title('FFT max')
    plt.legend(loc="upper left")
    #plt.xlim(0, len(highest_frequencies))

    # function to show plot
    SAVED_FILENAME = 'last_plot.png'
    plt.savefig(PATH + 'last_plot.png')
    plt.show()

    print('Don\'t forget to rename the scatter png named ' + SAVED_FILENAME)