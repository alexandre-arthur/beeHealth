from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense



DataLength = 8
dataset = loadtxt("Deeplearning\\Tests\\pima-indians-diabetes.csv", delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:DataLength]
Y = dataset[:,DataLength]

# define the keras model
model = Sequential()
model.add(Dense(12, input_shape=(DataLength,), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(X, Y, epochs=150, batch_size=10)

# evaluate the keras model
los, accuracy = model.evaluate(X, Y)
print(f'Accuracy: {accuracy*100} and Los : {los*100}')

# make class predictions with the model
guess = [1,126,60,0,0,30.1,0.349,47,1,1,93,70,31,0,30.4,0.315,23,0]
guess = dataset[:,0:DataLength]
predictions = (model.predict(guess) > 0.5).astype(int)
# summarize the first 5 cases
for i in range((int) (len(guess) / DataLength + 1)):
	print('%s => %d (expected %d)' % (guess[i].tolist(), predictions[i], y[i]))