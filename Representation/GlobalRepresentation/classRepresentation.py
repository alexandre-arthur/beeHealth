from abc import abstractmethod
import matplotlib.pyplot as plt
import librosa as rosa
import numpy as np


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                    Interface for all modes

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Representation:
    def __init__(self, text : str) -> None:
        self.text = text
        pass

    @abstractmethod
    def calculate(self, data, sr : int):
        pass

    def generic_plot(self, x, y, ax, xlabel, ylabel, xmin, xmax, ymin, ymax):
        if ax == None :
            plt.plot(x, y)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(self.text)
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
        else:
            ax.plot(x, y)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_title(self.text)
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

    def generic_simpler_plot(self, x, y, ax, xlabel, ylabel):
        xmin = min(x) * 1.01
        xmax = max(x) * 1.01
        ymin = min(y)
        ymax = max(y)
        self.generic_plot(x, y, ax, xlabel, ylabel, xmin, xmax, ymin, ymax)

    @abstractmethod
    def plot(self, x, y , ax) -> None:
        pass

    def plotfct(self, data, sr, ax):
        x, y = self.calculate(data, sr)
        self.plot(x, y, ax)

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
        super().__init__("Wave")

    def calculate(self, data, sr: int):
             # Get the duration of the file
        duration = len(data)

        # Get a list with all the time stamps
        time = np.arange(0, duration / sr, 1 / sr)

        return time, data 
    
    def plot(self, x, y , ax) -> None:
        time = x
        data = y
        xlabel = 'Time (s)'
        ylabel = 'Amplitude'
        title = self.text
        maxTime = max(time)
        ylim = max(data) * 1.01
        self.generic_plot(time, data, ax, xlabel, ylabel, 0, maxTime, -ylim, ylim)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           FFT

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class FFTclass(Representation):
    def __init__(self):
        super().__init__("FFT")

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
        title = self.text
        xlim = CUT_OFF_FREQUENCY
        ylim = max(y) * 1.01
        self.generic_plot(x, y, ax, xlabel, ylabel, 0, xlim, 0, ylim)

    def calculate_max(magnitudes, frequencies) -> float :
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
        super().__init__("Chroma feature")

    def calculate(self, data, sr : int):
        # Calculate the chroma feature
        chroma = rosa.feature.chroma_stft(y=data, sr=sr)
        return chroma, None

    def plot(self, x, y , ax):
        chroma = x
        xlabel = 'time'
        ylabel = 'chroma'
        title = self.text
        if ax == None:
            rosa.display.specshow(chroma, y_axis=ylabel, x_axis=xlabel)
        else:
            rosa.display.specshow(chroma, y_axis=ylabel, x_axis=xlabel, ax=ax)
            ax.set(title=title)

    def calculate_max(chroma) -> str :
        sum_chroma = [sum(c) for c in chroma]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_pitch = pitches[np.argmax(sum_chroma)]
        return max_pitch


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           MFCC

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class MFCCclass(Representation):
    def __init__(self):
        super().__init__("MFFC")
    
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
        title = self.text
        if ax == None:
            rosa.display.specshow(mfccs, sr=sr, x_axis=xlabel ,ax=ax)
        else:
            rosa.display.specshow(mfccs, sr=sr, x_axis=xlabel ,ax=ax)
            ax.set(title=title)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Chromatogram

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Spectrogramclass(Representation):
    def __init__(self):
        super().__init__("Spectrogram")

    def calculate(self, data, sr : int):
        # not useful but necessary
        return data, sr
    
    def plot(self, x, y , ax):
        data = x
        sr = y
        xlabel = 'Time'
        ylabel = 'Frequency (Hz)'
        title = self.text
        if ax == None:
            plt.specgram(data, Fs=sr, mode='psd') # psd = power spectral density
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
        else:
            ax.specgram(data, Fs=sr, mode='psd') # psd = power spectral density
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.set_title(title)

    def calculate_max(chroma) -> str :
        sum_chroma = [sum(c) for c in chroma]
        pitches = ['C', 'C#', 'D', 'D#','E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_pitch = pitches[np.argmax(sum_chroma)]
        return max_pitch

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        MFCC Delta

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class MFCCdeltaclass(Representation):
    def __init__(self) -> None:
        super().__init__("MFCC Delta")

    def calculate(self, data, sr : int):
        mfcc = rosa.feature.mfcc(y=data, sr=sr)
        mfcc_delta = rosa.feature.delta(mfcc)
        # not useful but necessary
        return mfcc_delta, None
    
    def plot(self, x, y , ax):
        mfcc_delta = x
        xlabel = 'time'
        title = self.text
        if ax == None:
            rosa.display.specshow(mfcc_delta, ax=ax, x_axis=xlabel)
        else:
            rosa.display.specshow(mfcc_delta, ax=ax, x_axis=xlabel)
            ax.set(title=title)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectral centroid

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class spectralcentroidclass(Representation):
    def __init__(self) -> None:
        super().__init__("Spectral Centroid")

    def calculate(self, data, sr : int):
        spectral_centroid = rosa.feature.spectral_centroid(y=data, sr=sr)

        return spectral_centroid, None
    
    def plot(self, x, y , ax):
        spectral_centroid = rosa.times_like(x)
        xlabel = 'time'
        ylabel = 'amp'
        self.generic_simpler_plot(spectral_centroid, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        ZCR

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ZCRClass(Representation):
    def __init__(self) -> None:
             super().__init__("Zero-crossing rate")

    def calculate(self, data, sr: int):
        zerocrossingrate = rosa.feature.zero_crossing_rate(data)
        return zerocrossingrate[0], range(len(zerocrossingrate[0]))
    
    def plot(self, x, y , ax):
        zerocrossingrate = rosa.times_like(x)
        xlabel = 'time'
        ylabel = 'Amplitude'
        self.generic_simpler_plot(zerocrossingrate, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Constant Q

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class ConstantQclass(Representation):
    def __init__(self) -> None:
        super().__init__("Constant Q")

    def calculate(self, data, sr: int):
        constantq = rosa.cqt(data, sr=sr)
        return constantq, sr
    
    def plot(self, x, y , ax):
        constantq = x
        sr = y
        xlabel = 'time'
        ylabel = 'chroma'
        title = self.text
        if ax == None:
            rosa.display.specshow(constantq, sr=sr, y_axis=ylabel, x_axis=xlabel)
        else:
            rosa.display.specshow(constantq, sr=sr, y_axis=ylabel, x_axis=xlabel, ax=ax)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Variable Q

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class VariableQclass(Representation):
    def __init__(self) -> None:
        super().__init__("Variable Q")

    def calculate(self, data, sr: int):
        chroma_vq = rosa.vqt(data, sr=sr)
        return chroma_vq, sr
    
    def plot(self, x, y , ax):
        chroma_vq = x
        sr = y
        xlabel = 'time'
        ylabel = 'chroma_fjs'
        title = self.text
        if ax == None:
            rosa.display.specshow(chroma_vq, sr=sr, y_axis=ylabel, x_axis=xlabel, intervals='ji5')
        else:
            rosa.display.specshow(chroma_vq, sr=sr, y_axis=ylabel, x_axis=xlabel, intervals='ji5', ax=ax)
            ax.set(title=title)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Energy normalized

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class EnergyNormalizedclass(Representation):
    def __init__(self) -> None:
        super().__init__("Energy Normalized")

    def calculate(self, data, sr: int):
        energy = rosa.feature.chroma_cens(y=data, sr=sr)
        return energy, sr

    def plot(self, x, y, ax) -> None:
        energy = x
        sr = y
        xlabel = 'time'
        ylabel = ''
        title = self.text
        if ax == None:
            rosa.display.specshow(energy, sr=sr, x_axis=xlabel)
        else:
            rosa.display.specshow(energy, sr=sr, x_axis=xlabel, ax=ax)
            ax.set(title=title)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Bandwidth

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Bandwidthclass(Representation):
    def __init__(self) -> None:
        super().__init__("Bandwidth")

    def calculate(self, data, sr: int):
        bandwidth = rosa.feature.spectral_bandwidth(y=data, sr=sr)
        return bandwidth, sr
    
    def plot(self, x, y, ax) -> None:
        bandwidth = rosa.times_like(x)
        sr = y
        xlabel = 'time'
        ylabel = 'log'
        self.generic_simpler_plot(bandwidth, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectral Contrast

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class SpectralContrastclass(Representation):
    def __init__(self) -> None:
        super().__init__("Spectral Contrast")
    
    def calculate(self, data, sr: int):
        spectral_contrast = rosa.feature.spectral_contrast(y=data, sr=sr)
        return spectral_contrast, sr
    
    def plot(self, x, y, ax) -> None:
        spectral_contrast = x
        sr = y
        xlabel = 'time'
        ylabel = 'log'
        title = self.text
        if ax == None:
            rosa.display.specshow(spectral_contrast, sr=sr, x_axis=xlabel)
        else:
            rosa.display.specshow(spectral_contrast, sr=sr, x_axis=xlabel, ax=ax)
            ax.set(title=title)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Spectral flatness

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class SpectralFlatnessclass(Representation):
    def __init__(self) -> None:
        super().__init__("Spectral Flatness")

    def calculate(self, data, sr: int):
        spectral_flatness = rosa.feature.spectral_flatness(y=data)
        return spectral_flatness, sr
    
    def plot(self, x, y, ax) -> None:
        spectral_flatness = rosa.times_like(x)
        sr = y
        xlabel = 'time'
        ylabel = 'log'
        title = self.text
        self.generic_simpler_plot(spectral_flatness, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Roll Off Frequency

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class SpectralRolloffclass(Representation):
    def __init__(self) -> None:
        super().__init__("Roll Off Frequency")

    def calculate(self, data, sr: int):
        roll_off_frequency = rosa.feature.spectral_rolloff(y=data, sr=sr)
        return roll_off_frequency, sr
    
    def plot(self, x, y, ax) -> None:
        roll_off_frequency = rosa.times_like(x)
        sr = y
        xlabel = 'time'
        ylabel = 'Hz'
        self.generic_simpler_plot(roll_off_frequency, x.T, ax, xlabel, ylabel)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                        Tonal centroid

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class TonalCentroidclass(Representation):
    def __init__(self) -> None:
        super().__init__("Tonal Centroid")

    def calculate(self, data, sr: int):
        tonal_centroid = rosa.feature.tonnetz(y=data, sr=sr)
        return tonal_centroid, sr
    
    def plot(self, x, y, ax) -> None:
        tonal_centroid = x
        sr = y
        xlabel = 'time'
        ylabel = 'tonnetz'
        title = self.text
        if ax == None:
            rosa.display.specshow(tonal_centroid, x_axis=xlabel, y_axis=ylabel, sr=sr)
        else:
            rosa.display.specshow(tonal_centroid, x_axis=xlabel, y_axis=ylabel, sr=sr, ax=ax)
            ax.set(title=title)

if __name__ == "__main__":
    func = TonalCentroidclass()


    FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\Ionian_mode_C.wav'
    # Create a new figure with only one axes
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    # Create a new representation
    representation = func
    # Load the audio file
    data, sr = rosa.load(PATH_NAME)
    # Calculate the representation
    representation.plotfct(data, sr, ax)
    # Show the plot
    plt.show()
