import os
from wave import open as waveOpen
from re import split as reSplit
import numpy as np
import math
import librosa as rosa
import time


##############################################################################################
#                                                                                            #
#              This file is used to create the dataset for the neural network                #
#                                                                                            #
##############################################################################################


#
#   To create a dataset with most of the data
#

def storeEverySampleButLast(audioPath : str, datasetPath : str, datasetName : str, sampleTime : int, timeVerbose : bool = False, verbose : bool = False):
    # Store every sample but the last one in a CSV file
    # @arguments : - audioPath : path of the audio files
    #              - datasetPath : path of the future dataset
    #              - datasetName : name of the future dataset
    #              - sampleTime : time of the sample in seconds
    #              - timeVerbose : do we want to print the time it took to parse each file (default : False)
    #              - verbose : do we want to print the time it took to parse each file (default : False)


    overallTime = time.time()
    sizeOfExtension = 4

    datasetPathFile = f"{datasetPath}{datasetName}"

    # Remove the file if it already exists
    if os.path.exists(datasetPathFile) :
        os.remove(datasetPathFile)

    # Only take files with lab files
    fileNames = []
    for fileName in os.listdir(audioPath):
        if "wav" in fileName:
            fileNames.append(fileName[:-sizeOfExtension])

    # Parse every file
    counter = 0
    for fileName in fileNames[1:-1]:
        counter += 1

        if verbose :
            print(f"Starting {fileName}")
        t = time.time()

        StoreFilesToCSV(f"{audioPath}{fileName}", datasetPath, datasetName, maxFreq=5000, sampleTime=sampleTime)
        
        if timeVerbose :
            print(f"{fileName} is done in {time.time() - t}s ({counter}/{len(fileNames[1:-1])}).")
        elif verbose :
            print(f"{fileName} is done.")

    if verbose or timeVerbose :
        print(f"Everything is done in {time.time() - overallTime}s")
        print(f"Size of a line : {int(55125 / 10 * sampleTime)}")

    # Remove the temporary file
    os.remove(f"{datasetPath}Processing.wav")


def StoreFilesToCSV(genericAudioPath : str, datasetPath : str, modelFileName : str, maxFreq : int = 5000, sampleTime : int = 10, timeVerbose : bool = False, verbose : bool = False):
    # Store the data of a file in a CSV file
    # @arguments : - genericAudioPath : name and path of the file to parse
    #              - datasetPath : path of the current file
    #              - modelFileName : name of the file in where we want to put the data (no extension)
    #              - maxFreq : maximum frequency to keep (default : 5000)
    #              - sampleTime : duration of the sample in seconds (default : 10)
    #              - timeVerbose : do we want to print the time (default : False)
    #              - verbose : do we want to print more information (default : False)


    # Paths
    dataFilePath = f"{genericAudioPath}.lab"
    audioFilePath = f"{genericAudioPath}.wav"
    datasetName = f"{datasetPath}{modelFileName}"
    tempAudioFilePath = f"{datasetPath}Processing.wav"

    # Read the lab file
    with open(dataFilePath, 'r') as reader:
        for lineNumber, line in enumerate(reader, start=1):
            # Check if there is "bee" or "nobee" in the line
            bee = checkBeeInString(line)
            if bee == None:
                continue

            # Get the begin stamps and the end stamps of the bee
            begin, end = getBeginAndEndOfBee(line, r'\t+')

            # Check if the duration is long enough
            if begin >= end - sampleTime - sampleTime :
                continue

            # Read the audio file and calculate the FFT
            for time in range(begin, end - sampleTime - sampleTime, sampleTime): # -sampleTime to avoid the end of the file then to keep sampleTime seconds for the test
                readPartOfAudio(audioFilePath, tempAudioFilePath, time, sampleTime, verbose=verbose)
                if timeVerbose :
                    print(f"time : {time} and duration : {sampleTime}")

            magnitudes = calculateFFT(tempAudioFilePath)
            magnitudes = magnitudes[:(int) (magnitudes.size/(20000 / maxFreq))] # Only upto a certain frequency

            # Write the data to the CSV file
            sampleNumber = int(55125 / 10 * sampleTime)
            writeToFileAsCSV(datasetName, magnitudes, bee, sampleNumber=sampleNumber)


#
#       Generic functions used in the dataset creation
#

def readPartOfAudio(sourceFileName : str, destinationFileName : str, startSecond : int, secondsToCopy : int, verbose : bool = False):
    # Read a part of an audio file and write it to another file
    # @arguments : - sourceFileName : the name of the file to read
    #              - destinationFileName : the name of the file to write
    #              - startSecond : the second at which to start reading
    #              - secondsToCopy : the number of seconds to copy


    # Check the arguments
    if secondsToCopy <= 0:
        raise Exception("secondsToCopy must be positive")
    if startSecond < 0:
        raise Exception("startSecond must be positive or equal to 0")

    # Open the file
    with waveOpen(sourceFileName, 'rb') as waveFile:
        framesPerSecond = waveFile.getframerate()

        # Calculate the number of frames to skip and to copy
        framesToSkip = int(startSecond * framesPerSecond)
        framesToCopy = int(secondsToCopy * framesPerSecond)

        # Go to the right position in the file
        try:
            waveFile.setpos(framesToSkip)
        except:
            print(f"Warning : Failed to set the position in the file {sourceFileName}, tried {startSecond} seconds max is {waveFile.getnframes() / waveFile.getframerate()}")

        # Read the frames and write them to the destination file
        with waveOpen(destinationFileName, 'wb') as outputFile:
            # duplicate the input file settings to the output file
            outputFile.setnchannels(waveFile.getnchannels())
            outputFile.setsampwidth(waveFile.getsampwidth())
            outputFile.setframerate(waveFile.getframerate())

            # Get the frames we want to copy
            framesWanted = waveFile.readframes(framesToCopy)

            # Write the new file
            outputFile.writeframes(framesWanted)

            if verbose :
                print(f"Copied {framesToCopy} frames from {framesToSkip} in {outputFile}")


def isBeeInString(string : str):
    # Check if there is "bee" in the string
    # @arguments : - string : string to check
    # @return : - True : if there is "bee"
    #           - False : if there is not "bee"


    return "bee" in string


def isNoBeeInString(string : str):
    # Check if there is "nobee" in the string
    # @arguments : - string : string to check
    # @return : - True : if there is "nobee"
    #           - False : if there is not "nobee"


    return "nobee" in string


def checkBeeInString(string : str):
    # Check if there is "bee" or "nobee" in the string
    # @arguments : - string : string to check
    # @return : - 1 : if there is "bee"
    #           - 0 : if there is "nobee"
    #           - None : if there is neither "bee" nor "nobee"


    if isBeeInString(string) and not isNoBeeInString(string):
        return 1
    elif isNoBeeInString(string):
        return 0
    else:
        return None


def getBeginAndEndOfBee(string : str, regex):
    # Get the begin and end of the bee in the string
    # @arguments : - string : string to check
    #              - regex : regex to use to split the string
    # @return : - begin : begin of the bee
    #           - end : end of the bee


    parts = reSplit(regex, string)
    beginStr = parts[0].replace(",", ".")
    endStr = parts[1].replace(",", ".")

    # Round the values
    begin = int(np.ceil(float(beginStr)))
    end = int(float(endStr))

    return begin, end


def calculateFFT(audioPath : str):
    # Calculate the FFT of an audio file
    # @arguments : - audioPath : path of the audio file
    # @return : - magnitudes : the magnitudes of the FFT coefficients
    # @raise : - Exception : if the file could not be loaded


    try :
        file, sr = rosa.load(audioPath)
    except:
        raise Exception(f"Failed to load the file {audioPath}")
    fftData = np.fft.fft(file)
    
    # Calculate the magnitudes of the FFT coefficients
    magnitudes = np.abs(fftData)
    return magnitudes


def writeToFileAsCSV(outputPath : str, data : list, bee : int, sampleNumber : int = 55125):
    # Write the data to a CSV file
    # @arguments : - outputPath : path of the file to write
    #              - datas : the magnitudes of the FFT coefficients
    #              - bee : the expected result
    #              - sampleNumber : the number of samples in the file (default : 55125)
    # @return : - True : if the data was written
    #           - False : if the data was not written
    # @raise : - Exception : if the data could not be serialized to a CSV


    # Serialize the data
    try :
        toWrite = ",".join(str(value) for value in data) + "," + str(bee) + "\n" # Transform as CSV
    except:
        raise Exception(f"Failed to serialize the data, got {data} and {bee}")
    
    # Write the data to the file
    with open(outputPath, "a") as file:
            if data.size != sampleNumber: # 55125 is the number of samples for 10 seconds
                print(f"Warning : Size of the data os {data.size}, expected {sampleNumber}")
                return False
            file.write(toWrite)
    return True
    
#
#       Functions used to create the verification using the last sample
#

def storeLastSample(audioPath : str, datasetPath : str, datasetName : str, sampleTime : int, timeVerbose : bool = False, verbose : bool = False):
    # Store the last sample of each bee file in a CSV file
    # @arguments : - audioPath : path of the audio files
    #              - datasetPath : path of the future dataset
    #              - datasetName : name of the future dataset
    #              - sampleTime : time of the sample in seconds
    #              - timeVerbose : do we want to print the time it took (default : False)
    #              - verbose : do we want to print (default : False)


    sizeOfExtension = 4

    datasetName = f"{datasetPath}{datasetName}"

    # Remove the file if it already exists
    if os.path.exists(datasetName):
        os.remove(datasetName)

    # Only take files with wav files
    fileNames = []
    for fileName in os.listdir(audioPath):
        if "wav" in fileName:
            fileNames.append(fileName[:-sizeOfExtension])

    # Parse every file
    counter = 0
    value = []
    for fileName in fileNames[1:-1]:
        counter += 1

        if verbose :
            print(f"Starting {fileName}")
        t = time.time()

        getLastSamplesInCSV(f"{audioPath}{fileName}", datasetPath, datasetName, 5)

        if timeVerbose :
            print(f"{fileName} is done in {time.time() - t}s ({counter}/{len(fileNames[1:-1])})")
        elif verbose :
            print(f"{fileName} is done.")
    return value


def getLastSamplesInCSV(audioFilePathName : str, datasetPath : str, modelFileName : str, sampleTime : int):
    # Store the last sample of a file in a CSV file
    # @arguments : - audioFilePathName : name of the file to parse
    #              - datasetPath : path of the current file
    #              - modelFileName : name of the file in where we want to put the data (no extension)


    maxFreq = 5000

    # Paths
    #genericFilePath = f"Audio/BeeDataset/RawFilesFromWeb/{audioFilePathName}"
    dataFilePath = f"{audioFilePathName}.lab"
    audioFilePath = f"{audioFilePathName}.wav"

    # Read the lab file
    with open(dataFilePath, 'r') as reader:
        for lineNumber, line in enumerate(reader, start=1):
            bee = checkBeeInString(line)
            if bee == None:
                continue

            begin, end = getBeginAndEndOfBee(line, r'\t+')

            if end - begin <= sampleTime:
                continue
            times = range(begin, end - sampleTime, sampleTime) # -10 to avoid the end of the file
            time = list(times)[-1]

            readPartOfAudio(audioFilePath, f"{datasetPath}Processing.wav", time, sampleTime)

            magnitudes = calculateFFT(f"{datasetPath}Processing.wav")
            magnitudes = magnitudes[:(int) (magnitudes.size/(20000 / maxFreq))] # Only upto a certain frequency

            sampleNumber = int(55125 / 10 * sampleTime)
            writeToFileAsCSV(f"{modelFileName}", magnitudes, bee, sampleNumber=sampleNumber)

if __name__ == "__main__":
    audioPath = "Audio/BeeDataset/RawFilesFromWeb/"
    datasetPath = "DeepLearning/NeuralHivework/HugeCSVHolder/"
    datasetName = "FastHoneyTransform2.csv"
    sampleSeconds = 5
    storeEverySampleButLast(audioPath, datasetPath, datasetName, sampleSeconds, verbose=True, timeVerbose=True)
    datasetName = "LastSamples.csv"
    storeLastSample(audioPath, datasetPath, datasetName, sampleSeconds, verbose=True, timeVerbose=True)
