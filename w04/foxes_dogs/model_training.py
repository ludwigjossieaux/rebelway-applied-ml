import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam
import pickle
import numpy as np
import time

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
  tf.config.experimental.set_memory_growth(gpu, True)

# https://poloclub.github.io/cnn-explainer/

X = np.asarray(pickle.load(open("X.pkl", "rb")))
y = np.asarray(pickle.load(open("y.pkl", "rb")))

X = X / 255.0 # Normalize pixel values

dense = [0, 1, 2]
layer_sizes = [32, 64, 128]
conv_layers = [1, 2, 3]

for dense_layer in dense:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            NAME = f"{conv_layer}-conv-{layer_size}-nodes-{dense_layer}-dense-{int(time.time())}"
            print(NAME)
            
            model = Sequential()
            
            model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:])) # input_shape "1:" from the second element onward
            model.add(Activation('relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            
            for l in range(conv_layer - 1):
                model.add(Conv2D(layer_size, (3, 3)))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2, 2)))
                
            model.add(Flatten()) # this converts our 3D feature maps to 1D feature vectors
            
            for _ in range(dense_layer):
                model.add(Dense(layer_size))
                model.add(Activation('relu'))
                
            model.add(Dense(1))
            model.add(Activation('sigmoid'))
            
            tensorboard = TensorBoard(log_dir=f'logs/{NAME}')
            
            model.compile(loss='binary_crossentropy',
                          optimizer=Adam(),
                          metrics=['accuracy'])
            
            model.fit(X, y, batch_size=32, epochs=10, validation_split=0.3, callbacks=[tensorboard])
            

