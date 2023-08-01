import ModelFunctions as model

path = f"DeepLearning/NeuralHivework/"
data_length = 55125
model.createAndStoreModelFromCSV(f"{path}/HugeCSVHolder/FastHoneyTransform.csv", f"{path}/ModelBeeHealth/model", [500, 300, 300, 300, 300], data_length=data_length, verbose=True)   

X, Y = model.loadCSVData(f"{path}HugeCSVHolder/LastSamples.csv", data_length=55125, verbose=True)
p, y = model.predict(model.loadModel(f"{path}/ModelBeeHealth/model"), X, Y, timeVerbose=True)

s = 0
for prediction, expected in zip(p.tolist(), y.tolist()) :
    if(prediction[0] == (int) (expected)):
        s += 1

print(f"Accuracy : {s / len(p) * 100}")