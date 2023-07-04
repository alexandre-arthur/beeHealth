import matplotlib.pyplot as plt
import numpy as np
import librosa as rosa
from scipy import signal
import classRepresentation

import Filters

FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
CUT_OFF_FREQUENCY = 4000

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           FUNCTIONS

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def getaudiofromfile(PATH_NAME : str):
    # Load the audio file
    data, sample_rate = rosa.load(PATH_NAME)

    # Convert the audio data to mono if it has multiple channels
    if len(data.shape) > 1:
        data = data.sum(axis=1) / data.shape[1]
    
    return data, sample_rate


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           MAIN

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def showAllRepresentation():
    # Load the audio file
    data, sample_rate = getaudiofromfile(PATH_NAME)

    # Filter the signal to get rid of all the noises
    data = Filters.sounddata_filter(data, sample_rate, maxFrequency = CUT_OFF_FREQUENCY)

    # Create the subplot for the graphs
    # to change the ratio : gridspec_kw={'width_ratios': [1, 2]}
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(9, 6))
    ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = axs

    # Change the two first subplot into 1
    ax1.remove()
    ax2.remove()
    gs = ax2.get_gridspec()
    ax = fig.add_subplot(gs[0, 0:])

    wave = classRepresentation.Waveclass()
    wave.plotfct(data, sample_rate, ax)

    fft = classRepresentation.FFTclass()
    fft.plotfct(data, sample_rate, ax3)

    chromatogram = classRepresentation.Chromatogramclass()
    chromatogram.plotfct(data, sample_rate, ax4)

    chromafeature = classRepresentation.ChromaFeatureclass()
    chromafeature.plotfct(data, sample_rate, ax5)

    mfcc = classRepresentation.MFCCclass()
    mfcc.plotfct(data, sample_rate, ax6)

    fig.tight_layout()
    fig.suptitle("Study of " + FILE_NAME)
    plt.show()

if __name__ == "__main__":
    allRepresentation()