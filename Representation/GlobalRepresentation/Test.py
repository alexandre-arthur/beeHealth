import matplotlib.pyplot as plt
import numpy as np
import librosa

y, sr = librosa.load(librosa.ex('trumpet'))

S, phase = librosa.magphase(librosa.stft(y=y))

cent = librosa.feature.spectral_centroid(y=y, sr=sr)

times = librosa.times_like(cent)

fig, ax = plt.subplots()

librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),

                         y_axis='log', x_axis='time', ax=ax)

ax.plot(times, cent.T, label='Spectral centroid', color='w')

ax.legend(loc='upper right')

ax.set(title='log Power spectrogram')

plt.show()
