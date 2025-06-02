#importing essential libraries
import numpy as np
import pandas as pd
import tensorflow.keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# importing the dataset

IMG_SIZE = (720,1280)
BATCH_SIZE = 32
DATASET_PATH =r"C:\Users\DELL\Desktop\OpenCode Tasks\PROJECTS\COMPUTER VISION PROJECT\digit_data"

datagen = ImageDataGenerator(validation_split=0.2, rescale=1./255)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='sparse',
    subset='training'
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='sparse',
    subset='validation'
)






#constructing the neural networks
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import ReLU,PReLU
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten

#Making the model
model=Sequential()
model.add(Flatten(input_shape=(720,1280,3)))
model.add(Dense(128,activation="relu"))
model.add(Dense(64,activation="relu"))
model.add(Dense(32,activation="relu"))
model.add(Dense(20  ,activation="relu"))
model.add(Dense(10,activation="softmax"))
model.compile(
    optimizer='adam',                           # Efficient optimizer
    loss='sparse_categorical_crossentropy',     # Suitable for integer labels
    metrics=['accuracy']                        # Measure accuracy
)

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)

model.save("mnist_ann.h5")