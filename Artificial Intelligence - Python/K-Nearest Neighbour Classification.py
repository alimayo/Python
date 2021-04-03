import pandas as pd
import numpy as np
from math import sqrt
import operator

def euclideanDistance(x1, x2, length):
    dist = 0
    for i in range(length):
        dist += (float(x1[i]) - float(x2[i]))**2
    return sqrt(dist)

def getKNeighbors(trainSet, test_ex, k):
    distances = []
    length = len(test_ex)-1
    for x in range(len(trainSet)):
        dist = euclideanDistance(test_ex, trainSet[x], length)
        distances.append((trainSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for i in range(len(neighbors)):
        resp = neighbors[i][-1]
        if resp in classVotes:
            classVotes[resp] += 1
        else:
            classVotes[resp] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

#use read_excel to read excel file 
train = pd.read_excel('TrainingSet.xlsx')
test = pd.read_excel('TestSet1.xlsx')

#convert excel file to array
train = np.asarray(train)
test = np.asarray(test)


for k in range(5,10,2):
    print('\n\nk = ', k)
    for i in range(len(test)):
        neighbors = getKNeighbors(train,test[i], k)
        pred = getResponse(neighbors) 
        print('For', test[i] , 'plant: ' , pred)
