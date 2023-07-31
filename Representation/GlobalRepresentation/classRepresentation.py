from abc import abstractmethod
import matplotlib.pyplot as plt
import librosa as rosa
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                    Interface for all modes

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Representation:
    def __init__(self, title : str, description : str) -> None:
        # Initialize the class with a title and a description
        # @arguments : - title : title of the Representation mode
        #              - description : description of the Representation mode
        self.title = title
        self.description = description
        pass

    @abstractmethod
    def calculate(self, data, sampleRate : int):
        # Calculate the data needed for the representation
        # @arguments : - data : 
        pass

    def generic_plot(self, x, y, ax, xlabel, ylabel, xmin, xmax, ymin, ymax):
        if ax == None :
            plt.plot(x, y)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(self.title)
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
        else:
            ax.plot(x, y)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_title(self.title)
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

    def generic_simpler_plot(self, x, y, ax, xlabel, ylabel):
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        self.generic_plot(x, y, ax, xlabel, ylabel, xmin, xmax, ymin, ymax)

    def generic_specshow(self, x, y_axis=None, x_axis=None, ylabel=None, xlabel=None, sampleRate=22050, ax=None):
        title = self.title
        if ax == None:
            rosa.display.specshow(x, y_axis=y_axis, x_axis=x_axis, sr=sampleRate)
        else:
            rosa.display.specshow(x, y_axis=y_axis, x_axis=x_axis, sr=sampleRate, ax=ax)
            if ylabel != None:
                ax.set_ylabel(ylabel)
            if xlabel != None:
                ax.set_xlabel(xlabel)
            ax.set_title(title)

    @abstractmethod
    def plot(self, x, y , ax) -> None:
        pass

    def getDescription(self) -> str:
        return self.description
    
    def getTitle(self) -> str:
        return self.title

    def plotfct(self, data, sampleRate, ax = None):
        x, y = self.calculate(data, sampleRate)
        self.plot(x, y, ax)

    def changeto(self, audio, sampleRate, fig, canva):
        fig.clear()
        newax = fig.add_subplot(111)
        self.plotfct(audio, sampleRate, newax)
        canva.draw_idle()

    def createImageFromPlot(self, pathAndFile, fig):
        fig.savefig(pathAndFile)

    def createImage(self, pathAndFile, data, sampleRate):
        fig, ax = plt.subplots(1, 1)
        self.plotfct(data, sampleRate, ax)
        self.createImageFromPlot(pathAndFile, fig)
        

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           Wave sound

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Waveclass(Representation):
    def __init__(self):
        desc = "Amplitude/Time : The waveform is the shape of the sound wave as it passes through the air. It is a graph of pressure against time. The waveform shows the changes in amplitude over a certain amount of time."
        super().__init__("Wave", desc)

    def calculate(self, data, sampleRate: int):
             # Get the duration of the file
        duration = len(data)

        # Get a list with all the time stamps
        time = np.arange(0, duration / sampleRate, 1 / sampleRate)

        return time, data 
    
    def plot(self, x, y , ax) -> None:
        time = x
        data = y
        xlabel = 'Time (s)'
        ylabel = 'Amplitude'
        maxTime = max(time)
        ylim = max(data) * 1.01
        self.generic_plot(time, data, ax, xlabel, ylabel, 0, maxTime, -ylim, ylim)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           FFT

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class FFTclass(Representation):
    def __init__(self):
        desc = "Magnitudes/Frequency : The FFT is a mathematical algorithm that determines the frequencies that make up the signal."
        super().__init__("FFT", desc)

    def calculate(self, data, sampleRate : int):
         # Apply FFT to the audio data
        fft_data = np.fft.fft(data)

        # Calculate the magnitudes of the FFT coefficients
        magnitudes = np.abs(fft_data)

        # Generate the corresponding frequencies for the FFT coefficients
        frequencies = np.fft.fftfreq(len(magnitudes), 1 / sampleRate)

        return frequencies, magnitudes
    
    def plot(self, x, y , ax):
        CUT_OFF_FREQUENCY = 4000

        xlabel = 'Frequency (Hz)'
        ylabel = 'Magnitudes'
        xlim = CUT_OFF_FREQUENCY
        ylim = max(y) * 1.01
        self.generic_plot(x, y, ax, xlabel, ylabel, 0, xlim, 0, ylim)
        maxFreq = self.calculate_max(y, x)
        ax.plot(maxFreq, max(y), 'ro')
        ax.title(maxFreq, max(y), '  Max frequency: ' + str(maxFreq) + ' Hz', horizontalalignment='left', verticalalignment='bottom')

    def calculate_max(self, magnitudes, frequencies) -> float :
        # Calculate the highest for a frequency
        argmax = np.array(magnitudes).argmax()
        high_freq = abs(frequencies[argmax])
        high_freq = round(high_freq, 2)
        return high_freq
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectral Bandwidth

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Bandwidthclass(Representation):
    def __init__(self) -> None:
        desc = "Amplitude/Time : The bandwidth is the range of frequencies that are present in the sound. It is calculated as the difference between the highest and lowest frequencies in the sound."
        super().__init__("Bandwidth", desc)

    def calculate(self, data, sampleRate: int):
        bandwidth = rosa.feature.spectral_bandwidth(y=data, sr=sampleRate)
        return bandwidth, sampleRate
    
    def plot(self, x, y, ax) -> None:
        bandwidth = rosa.times_like(x)
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Amplitude'
        self.generic_simpler_plot(bandwidth, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        ZCR

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ZCRClass(Representation):
    def __init__(self) -> None:
        desc = "Amplitude/Time : The zero-crossing rate is the rate of sign-changes along a signal, i.e., the rate at which the signal changes from positive to negative or back."
        super().__init__("Zero-crossing rate", desc)

    def calculate(self, data, sampleRate: int):
        zerocrossingrate = rosa.feature.zero_crossing_rate(data)
        return zerocrossingrate[0], range(len(zerocrossingrate[0]))
    
    def plot(self, x, y , ax):
        zerocrossingrate = rosa.times_like(x)
        xlabel = 'Time (s)'
        ylabel = 'Amplitude'
        self.generic_simpler_plot(zerocrossingrate, x.T, ax, xlabel, ylabel)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectral flatness

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class SpectralFlatnessclass(Representation):
    def __init__(self) -> None:
        desc = "Amplitude/Time : The spectral flatness is a measure to quantify how much noise-like a sound is, as opposed to being tone-like."
        super().__init__("Spectral Flatness", desc)

    def calculate(self, data, sampleRate: int):
        spectral_flatness = rosa.feature.spectral_flatness(y=data)
        return spectral_flatness, sampleRate
    
    def plot(self, x, y, ax) -> None:
        spectral_flatness = rosa.times_like(x)
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Amplitude'
        title = self.title
        self.generic_simpler_plot(spectral_flatness, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Roll Off Frequency

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class SpectralRolloffclass(Representation):
    def __init__(self) -> None:
        desc = "Frequency/Time : The roll-off frequency is the frequency below which a specified percentage of the total spectral energy, e.g. 85%, lies."
        super().__init__("Roll Off Frequency", desc)

    def calculate(self, data, sampleRate: int):
        roll_off_frequency = rosa.feature.spectral_rolloff(y=data, sr=sampleRate)
        return roll_off_frequency, sampleRate
    
    def plot(self, x, y, ax) -> None:
        roll_off_frequency = rosa.times_like(x)
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Frequency (Hz)'
        self.generic_simpler_plot(roll_off_frequency, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectrogram

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Spectrogramclass(Representation):
    def __init__(self):
        desc = "Frequency/Time : The spectrogram is a visual representation of the spectrum of frequencies of a signal as it varies with time."
        super().__init__("Spectrogram", desc)

    def calculate(self, data, sampleRate : int):
        # not useful but necessary
        return data, sampleRate
    
    def plot(self, x, y , ax):
        data = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Frequency (Hz)'
        title = self.title
        if ax == None:
            plt.specgram(data, Fs=sampleRate, mode='psd') # psd = power spectral density
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
        else:
            ax.specgram(data, Fs=sampleRate, mode='psd') # psd = power spectral density
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_title(title)

    def calculate_max(chroma) -> str :
        sum_chroma = [sum(c) for c in chroma]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_pitch = pitches[np.argmax(sum_chroma)]
        return max_pitch


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Chroma feature

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ChromaFeatureclass(Representation):
    def __init__(self):
        desc = "Pitch/Time : The chroma feature is a representation of the spectral energy where the bins represent the 12 equal-tempered pitch classes of western-type music (semitone spacing)."
        super().__init__("Chroma feature", desc)

    def calculate(self, data, sampleRate : int):
        # Calculate the chroma feature
        chroma = rosa.feature.chroma_stft(y=data, sr=sampleRate)
        return chroma, sampleRate

    def plot(self, x, y , ax):
        sampleRate = y
        chroma = x
        xlabel = 'Time (s)'
        ylabel = 'Pitch class'
        self.generic_specshow(chroma, y_axis='chroma', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)
        self.maxEachpoint(chroma, ax)

    def calculate_max(chroma) -> str :
        sum_chroma = [sum(c) for c in chroma]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_pitch = pitches[np.argmax(sum_chroma)]
        return max_pitch
    
    def maxEachpoint(self, chroma, ax):
        x = [[c[num] for c in chroma] for num in range(len(chroma[0]))]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        y = [np.argmax(c) for c in x]
        x = np.divide(range(len(y)), 43)

        xnew = np.linspace(min(x), max(x), len(x)) 

        spl = make_interp_spline(x, y, k=3)  # type: BSpline
        power_smooth = spl(xnew)

        #ax.plot(xnew, power_smooth)


        #ax.plot(x, y, 'r')
        #print(y)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Energy normalized

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class EnergyNormalizedclass(Representation):
    def __init__(self) -> None:
        desc = "Chroma/Time : "
        super().__init__("Energy Normalized", desc)

    def calculate(self, data, sampleRate: int):
        energy = rosa.feature.chroma_cens(y=data, sr=sampleRate)
        return energy, sampleRate

    def plot(self, x, y, ax) -> None:
        energy = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Chroma'
        self.generic_specshow(energy, y_axis='chroma', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           MFCC

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class MFCCclass(Representation):
    def __init__(self):
        desc = "Frequency/Time : The mel-frequency cepstrum (MFC) is a representation of the short-term power spectrum of a sound, based on a linear cosine transform of a log power spectrum on a nonlinear mel scale of frequency."
        super().__init__("MFFC", desc)
    
    def calculate(self, data, sampleRate : int):
        # Let's make and display a mel-scaled power (energy-squared) spectrogram
        S = rosa.feature.melspectrogram(y=data, sr=sampleRate, n_mels=128)

        # Convert to log scale (dB). We'll use the peak power as reference.
        mfccs = rosa.amplitude_to_db(S, ref=np.max)

        return mfccs, sampleRate
    
    def plot(self, x, y , ax):
        mfccs = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Frequency (Hz)'
        self.generic_specshow(mfccs, y_axis='mel', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        MFCC Delta

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class MFCCdeltaclass(Representation):
    def __init__(self) -> None:
        desc = "Frequency/Time : "
        super().__init__("MFCC Delta", desc)

    def calculate(self, data, sampleRate : int):
        mfcc = rosa.feature.mfcc(y=data, sr=sampleRate)
        mfcc_delta = rosa.feature.delta(mfcc)
        # not useful but necessary
        return mfcc_delta, sampleRate
    
    def plot(self, x, y , ax):
        mfcc_delta = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Frequency (Hz)'
        self.generic_specshow(mfcc_delta, y_axis='mel', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectral centroid

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class spectralcentroidclass(Representation):
    def __init__(self) -> None:
        desc = "Amplitude/Time : The spectral centroid indicates at which frequency the energy of a spectrum is centered upon or in other words It indicates where the ”center of mass” for a sound is located."
        super().__init__("Spectral Centroid", desc)

    def calculate(self, data, sampleRate : int):
        spectral_centroid = rosa.feature.spectral_centroid(y=data, sr=sampleRate)

        return spectral_centroid, None
    
    def plot(self, x, y , ax):
        spectral_centroid = rosa.times_like(x)
        xlabel = 'Time (s)'
        ylabel = 'Amplitude'
        self.generic_simpler_plot(spectral_centroid, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Constant Q

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ConstantQclass(Representation):
    def __init__(self) -> None:
        desc = "Chroma/Time : "
        super().__init__("Constant Q", desc)

    def calculate(self, data, sampleRate: int):
        constantq = rosa.cqt(data, sr=sampleRate)
        return constantq, sampleRate
    
    def plot(self, x, y , ax):
        constantq = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Chroma'
        self.generic_specshow(constantq, y_axis='chroma', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Variable Q

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class VariableQclass(Representation):
    def __init__(self) -> None:
        desc = "Chroma/Time : "
        super().__init__("Variable Q", desc)

    def calculate(self, data, sampleRate: int):
        chroma_vq = rosa.vqt(data, sr=sampleRate)
        return chroma_vq, sampleRate
    
    def plot(self, x, y , ax):
        chroma_vq = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Chroma_fjs'
        self.generic_specshow(chroma_vq, y_axis='chroma', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectral Contrast

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class SpectralContrastclass(Representation):
    def __init__(self) -> None:
        desc = "Frequency/Time : "
        super().__init__("Spectral Contrast", desc)
    
    def calculate(self, data, sampleRate: int):
        spectral_contrast = rosa.feature.spectral_contrast(y=data, sr=sampleRate)
        return spectral_contrast, sampleRate
    
    def plot(self, x, y, ax) -> None:
        spectral_contrast = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Frequency bands'
        self.generic_specshow(spectral_contrast, y_axis='log', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Tonal centroid

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class TonalCentroidclass(Representation):
    def __init__(self) -> None:
        desc = "Tonnetz/Time : "
        super().__init__("Tonal Centroid", desc)

    def calculate(self, data, sampleRate: int):
        tonal_centroid = rosa.feature.tonnetz(y=data, sr=sampleRate)
        return tonal_centroid, sampleRate
    
    def plot(self, x, y, ax) -> None:
        tonal_centroid = x
        sampleRate = y
        xlabel = 'Time (s)'
        ylabel = 'Tonnetz'
        self.generic_specshow(tonal_centroid, y_axis='tonnetz', x_axis='time', ylabel=ylabel, xlabel=xlabel, sampleRate=sampleRate, ax=ax)



if __name__ == "__main__":
    func = ChromaFeatureclass()


    FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\Ionian_mode_C.wav'
    # Create a new figure with only one axes
    #fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    # Create a new representation
    representation = func
    # Load the audio file
    data, sampleRate = rosa.load(PATH_NAME)
    func.plotfct(data, sampleRate)
    # Calculate the representation
    #representation.plotfct(data, sampleRate, ax)
    # Show the plot
    plt.show()
