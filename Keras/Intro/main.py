import os
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense
import os

modelFileName = 'model.json'
weightsFileName = 'model.h5'

dataset = np.loadtxt("pima-indians-diabetes.csv", delimiter=',')
X = dataset[:, :8]
Y = dataset[:, 8]
model = None
if modelFileName in os.listdir(os.getcwd()) \
   and weightsFileName in os.listdir(os.getcwd()):
    print 'File Loaded'
    json_file = open(modelFileName, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(weightsFileName)
else:
    model = Sequential()
    model.add(Dense(12, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])
# 9. Fit model on training data
model.fit(X, Y,
          batch_size=32, epochs=50, verbose=0)

# 10. Evaluate model on test data
score = model.evaluate(X, Y, verbose=0)
print score[1]
model_json = model.to_json()
with open(modelFileName, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(weightsFileName)
