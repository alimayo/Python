# SVM for multi-class classification using one-vs-one
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

#use read_excel to read excel file 
train = pd.read_excel('TrainingSet.xlsx')
test = pd.read_excel('TestSet1.xlsx')

#convert excel file to array
train = np.asarray(train)
test = np.asarray(test)
x_train = train[:,:-1]
y_train = train[:,-1]
x_test = test[:,:-1]
# define model
model = SVC()
# define ovo strategy
ovr = OneVsRestClassifier(model)
# fit model
ovr.fit(x_train, y_train)
# make predictions
yhat = ovr.predict(x_test)
print(yhat)
