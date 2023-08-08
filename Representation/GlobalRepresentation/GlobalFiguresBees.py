import matplotlib.pyplot as plt
import librosa as rosa

from ClassRepresentation import *
from GlobalClassRepresentation import GlobalClassRepresentation as allRepresentation
import Filters

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                           FUNCTIONS

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def getaudiofromfile(filePath : str, verbose : bool = False):
    # Load the audio file
    # @arguments : - filePath : path to the audio file
    # @return : - data : audio data
    #           - sampleRate : sample rate of the audio file


    data, sampleRate = rosa.load(filePath)

    # Convert the audio data to mono if it has multiple channels
    if len(data.shape) > 1:
        data = data.sum(axis=1) / data.shape[1]

    if verbose :
        print(f"Audio from {filePath} loaded")
    
    return data, sampleRate


def showAllRepresentation(filePath : str, cutOffFrequency : int = None):
    # Show all the representation of an audio file
    # @arguments : - filePath : path to the audio file
    #              - cutOffFrequency : frequency above which we want to filter the signal


    # Load the audio file
    data, sampleRate = getaudiofromfile(filePath)

    # Filter the signal to get rid of all the noises
    data = Filters.soundDataFilter(data, sampleRate, maxFrequency = cutOffFrequency)

    representation = allRepresentation().getAllModes()

    # Create the subplot for the graphs
    fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(20, 15))
    axes = sum([list(axes) for axes in axs], []) # Flatten the list of axes

    # Plot the representation
    for ax, rep in zip(axes, representation) :
        rep.plotfct(data, sampleRate, ax)

    fig.tight_layout()
    fig.suptitle("Study of " + filePath)
    plt.show()

if __name__ == "__main__":
    # An example of use
    fileName = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
    pathName = 'Audio\BeeDataset\OnlyBees\QueenBee\\' + fileName
    
    showAllRepresentation(pathName, cutOffFrequency=4000)