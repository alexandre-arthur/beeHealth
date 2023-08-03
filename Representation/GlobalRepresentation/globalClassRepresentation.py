from classRepresentation import *
import os
import librosa as rosa

class GlobalClassRepresentation():
    # Class that represents all the classes used in the class Representation
    
    def __init__(self):
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
        bandwidth = Bandwidthclass()
        spectralcontrast = SpectralContrastclass()
        spectralflatness = SpectralFlatnessclass()
        spectralrolloff = SpectralRolloffclass()
        tonalCentroid = TonalCentroidclass()
        self.existingMode = [wave, fft, bandwidth, zcr, spectralflatness, spectralrolloff, spectralcentroid, spectrogram, chromafeature, energynormalized, mfcc, mfccdelta, constantq, variableq, spectralcontrast, tonalCentroid]


    def getAllModes(self):
        # Get all the modes available
        # @return : - modes : list of the modes


        return self.existingMode


    def getAllPictures(self, path : str, audioFileName, verbose : bool = False):
        # Get all the pictures in a folder
        # @arguments : - path : path to the folder
        #              - verbose : do we want to print or not (default : False)
        

        # get the audio from the wav file 
        data, sampleRate = rosa.load(path + audioFileName)

        for mode in self.existingMode:
            filename = path + mode.getTitle().replace(" ", "_") + ".png"
            # Check if there is already images in the folder
            if os.path.isfile(filename) : # Images already exist
                print(f"Image {filename} already exist")
                return
                
            mode.createImage(filename, data, sampleRate)

        if verbose :
            print("All images created")



if __name__ == "__main__" :
    # Test the class
    path = "Representation/GlobalRepresentation/Test/"
    gcr = GlobalClassRepresentation()
    gcr.getAllPictures(path, verbose=True)
