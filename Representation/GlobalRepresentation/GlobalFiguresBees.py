import matplotlib.pyplot as plt
import numpy as np
import librosa as rosa
from scipy import signal    
from classRepresentation import *

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

    # Call all the different modes
    wave = Waveclass()
    fft = FFTclass()
    chromafeature = ChromaFeatureclass()
    spectrogram = Spectrogramclass()
    mfcc = MFCCclass()
    mfccdelta = MFCCdeltaclass()
    spectralcentroid = spectralcentroidclass()
    zcr = ZCRClass()
    constantq = ConstantQclass()
    variableq = VariableQclass()
    energynormalized = EnergyNormalizedclass()
    #bandwidth = Bandwidthclass()

    # Create the subplot for the graphs
    # to change the ratio : gridspec_kw={'width_ratios': [1, 2]}
    fig, axs = plt.subplots(nrows=4, ncols=3, figsize=(20, 15))
    ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax0), (ax10, ax11, ax12)) = axs

    # Change the two first subplot into 1
    """ax1.remove()
    ax2.remove()
    gs = ax2.get_gridspec()
    ax = fig.add_subplot(gs[0, 0:])
"""
    wave.plotfct(data, sample_rate, ax1)

    # mode with which we can study an audio file

    fft.plotfct(data, sample_rate, ax3)
    spectrogram.plotfct(data, sample_rate, ax4)
    chromafeature.plotfct(data, sample_rate, ax5)
    mfcc.plotfct(data, sample_rate, ax6)
    mfccdelta.plotfct(data, sample_rate, ax7)
    spectralcentroid.plotfct(data, sample_rate, ax8)
    zcr.plotfct(data, sample_rate, ax0)
    constantq.plotfct(data, sample_rate, ax10)
    variableq.plotfct(data, sample_rate, ax11)
    energynormalized.plotfct(data, sample_rate, ax12)
    #bandwidth.plotfct(data, sample_rate, ax2)

    fig.tight_layout()
    fig.suptitle("Study of " + FILE_NAME)
    plt.show()

if __name__ == "__main__":
    showAllRepresentation()