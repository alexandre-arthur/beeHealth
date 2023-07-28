import ModelFunctions as model

path = f"DeepLearning/NeuralHivework/"
data_length = 55125
model.createAndStoreModelFromCSV(f"{path}FastHoneyTransform.csv", f"{path}model", [300, 100, 100, 100], data_length=data_length, verbose=True)