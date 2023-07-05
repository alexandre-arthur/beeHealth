from abc import abstractmethod
import matplotlib.pyplot as plt
import librosa as rosa
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                    Interface for all modes

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Representation:
    def __init__(self, data, text : str) -> None:
        self.text = text
        pass

    @abstractmethod
    def calculate(self, data, sr : int):
        pass

    def generic_plot(self, x, y, ax, xlabel, ylabel, title, xmin, xmax, ymin, ymax):
        if ax == None :
            plt.plot(x, y)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
        else:
            ax.plot(x, y)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_title(title) # Let space for the big title
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

    @abstractmethod
    def plot(self, x, y , ax) -> None:
        pass

    def plotfct(self, data, sr, ax):
        x, y = self.calculate(data, sr)
        self.plot(x, y, ax)
        pass

    def changeto(self, audio, sr, fig, canva):
        fig.clear()
        newax = fig.add_subplot(111)
        self.plotfct(audio, sr, newax)
        canva.draw_idle()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           Wave sound

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Waveclass(Representation):
    def __init__(self):
        super().__init__(self, "Wave")

    def calculate(self, data, sr: int):
             # Get the duration of the file
        duration = len(data)

        # Get a list with all the time stamps
        time = range(duration)

        return time, data 
    
    def plot(self, x, y , ax) -> None:
        time = x
        data = y
        xlabel = 'Time (s)'
        ylabel = 'Amplitude'
        title = 'Wave sound'
        maxTime = max(time)
        ylim = max(data) * 1.01
        self.generic_plot(time, data, ax, xlabel, ylabel, title, 0, maxTime, -ylim, ylim)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           FFT

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class FFTclass(Representation):
    def __init__(self):
        super().__init__(self, "FFT")

    def calculate(self, data, sr : int):
         # Apply FFT to the audio data
        fft_data = np.fft.fft(data)

        # Calculate the magnitudes of the FFT coefficients
        magnitudes = np.abs(fft_data)

        # Generate the corresponding frequencies for the FFT coefficients
        frequencies = np.fft.fftfreq(len(magnitudes), 1 / sr)

        return frequencies, magnitudes
    
    def plot(self, x, y , ax):
        CUT_OFF_FREQUENCY = 4000

        xlabel = 'Frequency (Hz)'
        ylabel = 'Magnitudes'
        title = 'FFT'
        xlim = CUT_OFF_FREQUENCY
        ylim = max(y) * 1.01
        self.generic_plot(x, y, ax, xlabel, ylabel, title, 0, xlim, 0, ylim)

    def calculate_maxFFT(magnitudes, frequencies) -> float :
        # Calculate the highest for a frequency
        argmax = np.array(magnitudes).argmax()
        high_freq = abs(frequencies[argmax])
        high_freq = round(high_freq, 2)
        return high_freq


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Chroma feature

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ChromaFeatureclass(Representation):
    def __init__(self):
        super().__init__(self, "Chroma feature")

    def calculate(self, data, sr : int):
        # Calculate the chroma feature
        chroma = rosa.feature.chroma_stft(y=data, sr=sr)
        return chroma, None

    def plot(self, x, y , ax):
        chroma = x
        xlabel = 'time'
        ylabel = 'chroma'
        title = 'Chroma feature'
        if ax == None:
            rosa.display.specshow(chroma, y_axis=ylabel, x_axis=xlabel)
        else:
            rosa.display.specshow(chroma, y_axis=ylabel, x_axis=xlabel, ax=ax)
            ax.set(title=title)

    def calculate_maxchroma(chroma) -> str :
        sum_chroma = [sum(c) for c in chroma]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_pitch = pitches[np.argmax(sum_chroma)]
        return max_pitch


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           MFCC

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class MFCCclass(Representation):
    def __init__(self):
        super().__init__(self, "MFFC")
    
    def calculate(self, data, sr : int):
        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = rosa.feature.melspectrogram(y=data, sr=sr, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power as reference.
        mfccs = rosa.amplitude_to_db(S, ref=np.max)

        return mfccs, sr
    
    def plot(self, x, y , ax):
        mfccs = x
        sr = y
        xlabel = 'time'
        ylabel = 'index'
        title = 'Mel-frequency cepstrum'
        if ax == None:
            rosa.display.specshow(mfccs, sr=sr, x_axis=xlabel ,ax=ax)
        else:
            rosa.display.specshow(mfccs, sr=sr, x_axis=xlabel ,ax=ax)
            ax.set(title=title)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Chromatogram

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Chromatogramclass(Representation):
    def __init__(self):
        super().__init__(self, "Chroma feature")

    def calculate(self, data, sr : int):
        # Calculate the chroma feature
        chroma = rosa.feature.chroma_stft(y=data, sr=sr)
        return chroma, None
    
    def plot(self, x, y , ax):
        data = x
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

    def calculate_maxchroma(chroma) -> str :
        sum_chroma = [sum(c) for c in chroma]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_pitch = pitches[np.argmax(sum_chroma)]
        return max_pitch
