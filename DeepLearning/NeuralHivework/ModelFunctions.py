from keras.models import Sequential, model_from_json
from keras.layers import Dense
from numpy import loadtxt
from time import time
import os


##############################################################################################
#                                                                                            #
#       This file contains all the functions to create, store, load and use a ML model       #
#                                                                                            #
##############################################################################################


def loadCSVData(fileName : str, dataLength : int = 8, verbose : bool = False) :
    #Load the data from a csv file. 
    # @arguments : - fileName : must be a csv
    #              - datalength : number of column of the file - 1 (we don't include the results part of the csv)
    #              - verbose : do we want to print or not (default : False)
    # @return : - X : the data of the csv
    #           - Y : the expected result for each data


    if fileName[-4:] != ".csv":
        raise Exception("fileName must be a csv , file was : " + fileName)
    # load the datatset
    dataset = loadtxt(fileName, delimiter=",")

    # split into input (X : data) and output (Y : expected result) variables
    X = dataset[:,0:dataLength]
    Y = dataset[:,dataLength]

    return X, Y


def getLayersFromList(model, layers : list, dataLength : int) :
    # Create the layers of a model from a list, first layer will always be the number of input data
    # @arguments : - layers : list of the layers
    #              - dataLength : size of the input data
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    model.add(Dense(layers[0], input_dim=dataLength, activation='relu'))
    for i in range(1, len(layers)) :
        model.add(Dense(layers[i], activation='relu'))
    model.add(Dense(1, activation='sigmoid')) # sigmoid is used for binary classification (last one)


def createModel(X, Y, layers : list, dataLength : int, epochs : int = 150, batchSize : int = 10, verbose : bool = False) :
    # Create a model with the data
    # @arguments : - X : input of the model
    #              - Y : expected result
    #              - epochs : number of epochs (deault : 150)
    #              - batchSize : size of the batches in each epochs (default : 10)
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    t = time()
    # create model
    model = Sequential()
    getLayersFromList(model, layers, dataLength)

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(X, Y, epochs=epochs, batch_size=batchSize, verbose=verbose)

    # evaluate the model
    scores = model.evaluate(X, Y, verbose=verbose)
    if verbose :
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        print(f'Model created in {time() - t} seconds.')
    return model


def StoreJSONModel(model, fileName : str, verbose : bool = False) :
    # Store the model to a JSON file and a h5 file for the wheights
    # @arguments : - model : model to store
    #              - fileName : name of the file in where we want to put the data (no extension)
    #              - verbose : do we want to print or not (default : False)


    # serialize model to JSON
    modelJson = model.to_json()
    with open(fileName + ".json", "w") as jsonFile:
        jsonFile.write(modelJson)
        # serialize weights to HDF5
    model.save_weights(fileName + ".h5")
    if verbose :
        print("Saved model to disk")


def LoadJSONModel(fileName : str, verbose : bool = False):
    # Load a model from a json and a h5 file
    # @arguments : - fileName : name of the file where the data is stored without the extension
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    # open the json file
    jsonFile = open(fileName+'.json', 'r')
    loadedModelJson = jsonFile.read()
    jsonFile.close()
    loadedModel = model_from_json(loadedModelJson)
    # load weights into new model
    loadedModel.load_weights(fileName + ".h5")
    if verbose :
        print("Loaded model from disk")
    return loadedModel


def loadModel(fileName : str, verbose : bool = False):
    # Load a model from a json file and compile it
    # @arguments : - fileName : name of the file where the data is stored without the extension
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    t = time()
    # load json and create model
    loadedModel = LoadJSONModel(fileName, verbose=verbose)

    # evaluate loaded model on test data
    loadedModel.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    if verbose :
        print(f'Model loaded in {time() - t} seconds.')

    return loadedModel


def evaluateModel(model, X, Y, verbose : bool = False):
    # Evaluate a model
    # @arguments : - model : model to store
    #              - X : input of the model
    #              - Y : expected result
    #              - verbose : do we want to print or not (default : False)


    # Evaluate the model
    scores = model.evaluate(X, Y, verbose=verbose)
    if verbose :
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


def predict(model, X_guess : list, Y_guess : list, verbose : bool = False, timeVerbose : bool = False):
    # predict a value using a ML model
    # @arguments : - model : model to use
    #              - X_guess : input of the model
    #              - Y_guess : expected result
    #              - dataLength : size of the array - 1, must be the same as the model input size
    #              - verbose : do we want to print or not (default : False)
    #              - timeVerbose : do we want to print the time it took to predict (default : False)


    # make class predictions with the model
    predictions = (model.predict(X_guess) > 0.5).astype(int)
    t = time()
    if verbose or timeVerbose:
        for i in range((int) (len(X_guess))):
            if timeVerbose :
                print(f"Got {predictions[i]}, expected {Y_guess[i]} in {time() - t} seconds.")
            elif verbose :
                print('Got %d, expected %d' % (predictions[i], Y_guess[i]))
    return predictions, Y_guess


def prediction(model, guess : list, dataLength : int, verbose : bool = False):
    # predict a value using a ML model
    # @arguments : - model : model to use
    #              - guess : numpy array with each line in a different sub array
    #              - dataLength : size of the array - 1, must be the same as the model input size
    #              - verbose : do we want to print or not (default : False)


    X_guess = guess[:,0:dataLength]
    Y_guess = guess[:,dataLength]
    # make class predictions with the model
    predict(model, X_guess, Y_guess, verbose=verbose)


def createAndStoreModelFromCSV(inputFileName : str, outputFileName : str, layers : list, dataLength : int, epochs : int = 150, batchSize : int = 10, verbose : bool = False) :
    # Create and then store a ML model
    # @arguments : - inputFileName : the csv file with the data
    #              - outputFileName : the name of the json and the h5 with the data without an extension
    #              - dataLength : the number of information in each column of the csv - 1
    #              - verbose : do we want to print or not (default : False)


    X, Y = (0, 0)
    try :
        X, Y = loadCSVData(inputFileName, dataLength=dataLength, verbose=verbose)
    except:
        raise Exception(f"Unable to load the data, verify if the file {inputFileName} exists.")

    model = createModel(X, Y, layers, dataLength, epochs=epochs, batchSize=batchSize, verbose=verbose)
    evaluateModel(model, X, Y, verbose=verbose)
    StoreJSONModel(model, outputFileName, verbose=verbose)

if __name__ == "__main__" :
    createAndStoreModelFromCSV(f"Deeplearning/NeuralHivework/HugeCSVHolder/FastHoneyTransform2.csv", f"Deeplearning/NeuralHivework/ModelBeeHealth/model2", [5000, 3000, 1000, 500, 500], dataLength=10, verbose=True)   
