import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def convert_to_one_hot(Y, C):
    Y = np.eye(C)[Y.reshape(-1)].T
    return Y

#use read_excel to read excel file 
train = pd.read_excel('TrainingSet.xlsx')
test = pd.read_excel('TestSet1.xlsx')

#convert excel file to array
train = np.asarray(train)
x_train = train[:,:-1]
x_train = x_train.astype("float32")
y_train = train[:,-1]

index = 0
word_to_index = {}
for i in range(len(y_train)):
    if y_train[i].lower() in word_to_index:
        # already seen
        continue
    word_to_index[y_train[i].lower()] = index
    index += 1
for i in range(len(y_train)):
    if y_train[i].lower() in word_to_index:
        y_train[i] =  word_to_index[y_train[i].lower()]
        
nb_classes = 3
targets = np.array([y_train]).reshape(-1)
y_train_one = np.eye(nb_classes)[np.array(targets,dtype = "int8")]

test = np.asarray(test)

inputs = keras.Input(shape=(4,), name="digits")
x = layers.Dense(8, activation="relu", name="dense_1")(inputs)
x = layers.Dense(10, activation="relu", name="dense_2")(x)
outputs = layers.Dense(3, activation="softmax", name="predictions")(x)

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("Fit model on training data")
history = model.fit(
    x_train,
    y_train_one,
    batch_size=32,
    epochs=60,
)

print()
predictions = model.predict(test[:,:-1])
m = np.zeros_like(predictions)
m[np.arange(len(predictions)), predictions.argmax(1)] = 1
outs = [np.where(r==1)[0][0] for r in m]
for i in range(len(outs)):
    for key,value in word_to_index.items():
        if outs[i] == value:
            outs[i] = key
print(outs)
