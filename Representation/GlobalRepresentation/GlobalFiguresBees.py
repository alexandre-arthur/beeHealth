import matplotlib.pyplot as plt
import numpy as np
import librosa as rosa
from scipy import signal

FILE_NAME = 'Audio_file_3.wav'
PATH_NAME = 'Representation\Audio\AudioLessThan2Mins\\' + FILE_NAME

# Load the audio file
data, sample_rate = rosa.load(PATH_NAME)

# Filtering the audio signal
CUT_OFF_FREQUENCY = 1000
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

# Generate the corresponding frequencies for the FFT coefficients
frequencies = np.fft.fftfreq(len(magnitudes), 1 / sample_rate)

# Calculate the angle FFT of the signal
phase = np.angle(data)

# Calculate the chromtoagram 
S = np.abs(rosa.stft(magnitudes, n_fft=4096))**2
chroma = rosa.feature.chroma_stft(S=S, sr=sample_rate)

# Calculate the MFCC
mfccs = rosa.feature.mfcc(y=data, sr=sample_rate)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           PLOTTING

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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
ax.plot(time, data)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.set_title(' ')
ax.set_xlim(0, duration)
ax.set_ylim(- max(data) * 1.01, max(data) * 1.01)
#plt.axis([0, 1000, 0, max(magnitudes) * 1.01])
#ax.grid(True)

# Plot the FFT
ax = ax3
ax.plot(frequencies, magnitudes)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude')
ax.set_title('FFT')
ax.set_xlim(0, CUT_OFF_FREQUENCY)
ax.set_ylim(0, max(magnitudes) * 1.01)

# plot the chromagram
ax = ax4
ax.specgram(data, mode='psd') # psd = power spectral density
ax.set_xlabel('Time')
ax.set_ylabel('Frequency (Hz)')
ax.set_title('Chromatogram')
#fig.colorbar(img, ax=ax)

#Displaying  the MFCCs:
ax = ax5
img = rosa.display.specshow(mfccs, sr=sample_rate, x_axis='time', ax=ax)
ax.set(title='MFCC')
fig.colorbar(img, ax=ax)

ax = ax6
img = rosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax)
ax.set(title='Chroma feature')
fig.colorbar(img, ax=ax)

fig.tight_layout()
fig.suptitle("Study of " + FILE_NAME)
plt.show()