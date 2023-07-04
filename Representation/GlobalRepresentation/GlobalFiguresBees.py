import matplotlib.pyplot as plt
import numpy as np
import librosa as rosa
from scipy import signal

import Filters

FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
CUT_OFF_FREQUENCY = 4000

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           FUNCTIONS

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Maths

def getaudiofromfile(PATH_NAME : str):
    # Load the audio file
    data, sample_rate = rosa.load(PATH_NAME)

    # Convert the audio data to mono if it has multiple channels
    if len(data.shape) > 1:
        data = data.sum(axis=1) / data.shape[1]
    
    return data, sample_rate

def calculate_FFT(data, sample_rate):
    # Apply FFT to the audio data
    fft_data = np.fft.fft(data)

    # Calculate the magnitudes of the FFT coefficients
    magnitudes = np.abs(fft_data)

    # Generate the corresponding frequencies for the FFT coefficients
    frequencies = np.fft.fftfreq(len(magnitudes), 1 / sample_rate)

    return magnitudes, frequencies

def calculate_time(data):
     # Get the duration of the file
    duration = len(data)

    # Get a list with all the time stamps
    time = range(duration)

    return time

def calculate_maxFFT(magnitudes, frequencies) -> float :
    # Calculate the highest for a frequency
    argmax = np.array(magnitudes).argmax()
    high_freq = abs(frequencies[argmax])
    high_freq = round(high_freq, 2)
    return high_freq

def calculate_chroma(data, sr : int):
    # Calculate the chroma feature
    chroma = rosa.feature.chroma_stft(y=data, sr=sr)
    return chroma

def calculate_maxchroma(chroma) -> str :
        sum_chroma = [sum(c) for c in chroma]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_pitch = pitches[np.argmax(sum_chroma)]
        return max_pitch

def calculate_MFCC(data, sr : int):
     # Let's make and display a mel-scaled power (energy-squared) spectrogram
    S = rosa.feature.melspectrogram(y=data, sr=sr, n_mels=128)

    # Convert to log scale (dB). We'll use the peak power as reference.
    mfccs = rosa.amplitude_to_db(S, ref=np.max)

    return mfccs

# Plots
def generic_plot(x, y, ax, xlabel, ylabel, title, xmin, xmax, ymin, ymax):
    if ax == None :
        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title) # Let space for the big title
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
    else:
        ax.plot(x, y)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title) # Let space for the big title
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

def plot_wave(time, data, ax):
    xlabel = 'Time (s)'
    ylabel = 'Amplitude'
    title = 'Wave sound'
    maxTime = max(time)
    ylim = max(data) * 1.01
    generic_plot(time, data, ax, xlabel, ylabel, title, 0, maxTime, -ylim, ylim)

def plotfct_wave(data, ax=None):
    time = calculate_time(data)
    plot_wave(time, data, ax)

def plot_FFT(magnitudes, frequencies, ax=None):
    CUT_OFF_FREQUENCY = 4000

    xlabel = 'Frequency (Hz)'
    ylabel = 'Magnitudes'
    title = 'FFT'
    xlim = CUT_OFF_FREQUENCY
    ylim = max(magnitudes) * 1.01
    generic_plot(frequencies, magnitudes, ax, xlabel, ylabel, title, 0, xlim, 0, ylim)

def plotfct_FFT(data, sr, ax):
    magnitudes, frequencies = calculate_FFT(data, sr)
    plot_FFT(magnitudes, frequencies, ax)


def plot_chromatogram(data, ax=None):
    xlabel = 'Time'
    ylabel = 'Frequency (Hz)'
    title = 'Chromatogram'
    if ax == None:
        plt.specgram(data, mode='psd') # psd = power spectral density
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
    else:
        ax.specgram(data, mode='psd') # psd = power spectral density
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

def plotfct_chromatogram(data, ax):
    plot_chromatogram(data, ax)

def plot_chromafeature(chroma, ax=None, fig=None):
    xlabel = 'time'
    ylabel = 'chroma'
    title = 'Chroma feature'
    if ax == None:
        rosa.display.specshow(chroma, y_axis=ylabel, x_axis=xlabel)
    else:
        img = rosa.display.specshow(chroma, y_axis=ylabel, x_axis=xlabel, ax=ax)
        ax.set(title=title)
        if fig != None :
            fig.colorbar(img, ax=ax)

def plotfct_chromafeature(data, sr, ax):
    chroma = calculate_chroma(data, sr)
    plot_chromafeature(chroma, ax)

def plot_MFCC(mfccs, sr, ax=None, fig=None):
    xlabel = 'time'
    title = 'MFCC'
    if ax == None:
        rosa.display.specshow(mfccs, sr=sr, x_axis=xlabel ,ax=ax)
    else:
        img = rosa.display.specshow(mfccs, sr=sr, x_axis=xlabel ,ax=ax)
        ax.set(title=title)
        if fig != None :
            fig.colorbar(img, ax=ax)

def plotfct_MFCC(data, sr, ax):
    mfccs = calculate_MFCC(data, sr)
    plot_MFCC(mfccs, sr, ax)
    


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           MAIN

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == "__main__":
    # Load the audio file
    data, sample_rate = getaudiofromfile(PATH_NAME)

    # Filter the signal to get rid of all the noises
    data = Filters.sounddata_filter(data, sample_rate, maxFrequency = CUT_OFF_FREQUENCY)

    time = calculate_time(data)

    magnitudes, frequencies = calculate_FFT(data, sample_rate)

    # Calculate the highest for a frequency
    high_freq = calculate_maxFFT(magnitudes, frequencies)

    # Calculate the angle FFT of the signal
    # phase = np.angle(data)

    # Calculate the chroma feature
    chroma = calculate_chroma(data, sample_rate)
    max_pitch = calculate_maxchroma(chroma)

    mfccs = calculate_MFCC(data, sample_rate)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           PLOTTING

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == "__main__":
    # Create the subplot for the graphs
    # to change the ratio : gridspec_kw={'width_ratios': [1, 2]}
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(9, 6))
    ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = axs

    # Change the two first subplot into 1
    ax1.remove()
    ax2.remove()
    gs = ax2.get_gridspec()
    ax = fig.add_subplot(gs[0, 0:])

    # plot the sound wave
    plot_wave(time, data, ax)

    # Plot the FFT
    ax = ax3
    plot_FFT(magnitudes, frequencies, ax)

    # plot the chromatogram
    ax = ax4
    plot_chromatogram(data, ax)

    #Displaying  the MFCCs:
    ax = ax5
    plot_MFCC(mfccs, sample_rate, ax, fig)

    # Displaying the chroma feature
    ax = ax6
    plot_chromafeature(chroma, ax, fig)

    fig.tight_layout()
    fig.suptitle("Study of " + FILE_NAME)
    plt.show()