from keras.models import Sequential, model_from_json
from keras.layers import Dense
from numpy import loadtxt
from time import time


##############################################################################################
#                                                                                            #
#       This file contains all the functions to create, store, load and use a ML model       #
#                                                                                            #
##############################################################################################


def loadCSVData(filename : str, data_length : int = 8, verbose : bool = False) :
    #Load the data from a csv file. 
    # @arguments : - filename : must be a csv
    #              - datalength : number of column of the file - 1 (we don't include the results part of the csv)
    #              - verbose : do we want to print or not (default : False)
    # @return : - X : the data of the csv
    #           - Y : the expected result for each data


    if filename[-4:] != ".csv":
        raise Exception("filename must be a csv , file was : " + filename)
    # load the datatset
    dataset = loadtxt(filename, delimiter=",")

    # split into input (X : data) and output (Y : expected result) variables
    X = dataset[:,0:data_length]
    Y = dataset[:,data_length]

    return X, Y


def getLayersFromList(model, layers : list, data_length : int) :
    # Create the layers of a model from a list
    # @arguments : - layers : list of the layers
    #              - data_length : size of the input data
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    model.add(Dense(layers[0], input_dim=data_length, activation='relu'))
    for i in range(1, len(layers)) :
        model.add(Dense(layers[i], activation='relu'))
    model.add(Dense(1, activation='sigmoid')) # sigmoid is used for binary classification (last one)


def createModel(X, Y, layers : list, data_length : int, epochs : int = 150, batch_size : int = 10, verbose : bool = False) :
    # Create a model with the data
    # @arguments : - X : input of the model
    #              - Y : expected result
    #              - epochs : number of epochs (deault : 150)
    #              - batch_size : size of the batches in each epochs (default : 10)
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    t = time()
    # create model
    model = Sequential()
    getLayersFromList(model, layers, data_length)

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(X, Y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    # evaluate the model
    scores = model.evaluate(X, Y, verbose=verbose)
    if verbose :
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        print(f'Model created in {time() - t} seconds.')
    return model


def StoreJSONModel(model, filename : str, verbose : bool = False) :
    # Store the model to a JSON file and a h5 file for the wheights
    # @arguments : - model : model to store
    #              - filename : name of the file in where we want to put the data (no extension)
    #              - verbose : do we want to print or not (default : False)


    # serialize model to JSON
    model_json = model.to_json()
    with open(filename + ".json", "w") as json_file:
        json_file.write(model_json)
        # serialize weights to HDF5
    model.save_weights(filename + ".h5")
    if verbose :
        print("Saved model to disk")


def LoadJSONModel(filename : str, verbose : bool = False):
    # Load a model from a json and a h5 file
    # @arguments : - filename : name of the file where the data is stored without the extension
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    # open the json file
    json_file = open(filename+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(filename+".h5")
    if verbose :
        print("Loaded model from disk")
    return loaded_model


def loadModel(filename : str, verbose : bool = False):
    # Load a model from a json file and compile it
    # @arguments : - filename : name of the file where the data is stored without the extension
    #              - verbose : do we want to print or not (default : False)
    # @return : - model : the model


    t = time()
    # load json and create model
    loaded_model = LoadJSONModel(filename, verbose=verbose)

    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    if verbose :
        print(f'Model loaded in {time() - t} seconds.')

    return loaded_model


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
    #              - data_length : size of the array - 1, must be the same as the model input size
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


def prediction(model, guess : list, data_length : int, verbose : bool = False):
    # predict a value using a ML model
    # @arguments : - model : model to use
    #              - guess : numpy array with each line in a different sub array
    #              - data_length : size of the array - 1, must be the same as the model input size
    #              - verbose : do we want to print or not (default : False)


    X_guess = guess[:,0:data_length]
    Y_guess = guess[:,data_length]
    # make class predictions with the model
    predict(model, X_guess, Y_guess, verbose=verbose)


def createAndStoreModelFromCSV(input_filename : str, output_filename : str, layers : list, data_length : int, verbose : bool = False) :
    # Create and then store a ML model
    # @arguments : - input_filename : the csv file with the data
    #              - output_filename : the name of the json and the h5 with the data without an extension
    #              - data_length : the number of information in each column of the csv - 1
    #              - verbose : do we want to print or not (default : False)


    X, Y = (0, 0)
    try :
        X, Y = loadCSVData(input_filename, data_length=data_length, verbose=verbose)
    except:
        print(f"Unable to load the data, verify if the file {input_filename} exists.")
        return

    model = createModel(X, Y, layers, data_length, verbose=verbose)
    evaluateModel(model, X, Y, verbose=verbose)
    StoreJSONModel(model, output_filename, verbose=verbose)
