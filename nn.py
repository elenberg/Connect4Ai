from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np
from filereader import FileReader


ff = FileReader()
ff.get_data()
X = np.array(ff.states)
y = np.array(ff.outputs)

model = Sequential()
model.add(Dense(124, input_dim=42))
model.add(Activation('sigmoid'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

sgd = SGD(lr=0.1)
model.compile(loss='mse', optimizer=sgd)

model.fit(X, y, show_accuracy=True, batch_size=1, nb_epoch=500)
model.save('my_model.h5')
# print(model.predict_proba(X))

# model = load_model('my_model.h5')
# print(model.predict(X))
# print("Actual", y)