import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import seaborn as sn
import matplotlib.pyplot as plt

#use read_excel to read excel file 
ts = pd.read_excel(r'TrainingSet.xlsx')
tests = pd.read_excel(r'TestSet1.xlsx')

#convert excel file to data frame
x_train = pd.DataFrame(ts, columns= ['leaf.length','leaf.width','flower.length','flower.width','plant'])
x_test = pd.DataFrame(tests, columns= ['leaf.length','leaf.width','flower.length','flower.width','plant'])

#separate predictors from category
features = x_train[['leaf.length','leaf.width','flower.length','flower.width']]
result = x_train['plant']
testfeatures = x_test[['leaf.length','leaf.width','flower.length','flower.width']]

#apply random forest classification varrying the number of trees
rf1 = RandomForestClassifier(n_estimators=100)  #100 trees
rf1.fit(features,result)
rf2 = RandomForestClassifier(n_estimators=300)
rf2.fit(features,result)
rf3 = RandomForestClassifier(n_estimators=500)
rf3.fit(features,result)

#predict results for test  set
prediction1 = rf1.predict(testfeatures) 
prediction2 = rf2.predict(testfeatures)
prediction3 = rf3.predict(testfeatures) 

#print results for each case
print ('Predicted Result with 100 trees: \n', prediction1,"\n") 
print ('Predicted Result with 300 trees: \n', prediction2,"\n")
print ('Predicted Result with 500 trees: \n', prediction3,"\n")

#calculate importance of individual features
print ("Feature Importance:")
(pd.Series(rf1.feature_importances_, index=features.columns)
   .nlargest(4)
   .plot(kind='bar'))
