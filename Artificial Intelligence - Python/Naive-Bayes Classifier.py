import numpy as np

#We are training the classifier with respect to the dataset given 
def train(data):

    c_labels = data[:,0] #class labels
    features = data[:, 1:] #features

    prob_S = len(c_labels[c_labels[:]=="senior"])/len(c_labels)
    prob_J = len(c_labels[c_labels[:]=="junior"])/len(c_labels)
    print("\nProbability of Senior:")
    print(prob_S)
    print("\nProbability of Junior:")
    print(prob_J) 

    #initializing conditional probabilities
    dep = np.unique(features[:,0])
    ages = np.unique(features[:,1])
    sal = np.unique(features[:,2])
   
    cond_ProbDep = np.zeros(( len(np.unique(c_labels)), len(np.unique(features[:,0]))  ))
    cond_ProbSal = np.zeros(( len(np.unique(c_labels)), len(np.unique(features[:,1]))  ))
    cond_ProbAge = np.zeros(( len(np.unique(c_labels)), len(np.unique(features[:,2]))  ))

    #calculating conditional probabilities of department, age group and salary
    i=0
    nDep = len(dep)
    nAge = len(ages)
    nSal = len(sal)

    for d_type in dep:
        cond_ProbDep[0][i] = (len(data[(data[:,0]=="senior") & (data[:,1]==d_type)]) + 1) / (len(c_labels[c_labels[:]=="senior"]) + (1*nDep))
        cond_ProbDep[1][i] = (len(data[(data[:,0]=="junior") & (data[:,1]==d_type)]) + 1) / (len(c_labels[c_labels[:]=="junior"]) + (1*nDep))
        i = i+1
    i=0
    for value in ages:
        cond_ProbAge[0][i] = (len(data[(data[:,0]=="senior") & (data[:,2]==value)]) + 1) / (len(c_labels[c_labels[:]=="senior"]) + (1*nAge))
        cond_ProbAge[1][i] = (len(data[(data[:,0]=="junior") & (data[:,2]==value)]) + 1) / (len(c_labels[c_labels[:]=="junior"]) + (1*nAge))
        i = i+1
    i=0
    for value in sal:
        cond_ProbSal[0][i] = (len(data[(data[:,0]=="senior") & (data[:,3]==value)]) + 1) / (len(c_labels[c_labels[:]=="senior"]) + (1*nSal))
        cond_ProbSal[1][i] = (len(data[(data[:,0]=="junior") & (data[:,3]==value)]) + 1) / (len(c_labels[c_labels[:]=="junior"]) + (1*nSal))
        i = i+1

    print("\nAttributes probabilities in accordance with senior and junior respectively: ")
    print("\nConditional Probability Department:")
    print(cond_ProbDep)
    print("\nConditional Probability Age:")
    print(cond_ProbAge)
    print("\nConditional Probability Salary:")
    print(cond_ProbSal)

    return prob_S, prob_J, cond_ProbDep, cond_ProbAge, cond_ProbSal
 
def predict(data, features, prob_S, prob_J, cond_ProbDep, cond_ProbAge, cond_ProbSal):

    #initializing conditional probabilities
    dep = np.unique(features[:,0])
    ages = np.unique(features[:,1])
    sal = np.unique(features[:,2])
   
    prob_S =prob_S*(cond_ProbDep[0][dep[:]==data[0]])*(cond_ProbAge[0][ages[:]==data[1]])*(cond_ProbSal[0][sal[:]==data[2]])
    print("\nProbability of being a senior:")
    print(prob_S)
    prob_J =prob_J*(cond_ProbDep[1][dep[:]==data[0]])*(cond_ProbAge[1][ages[:]==data[1]])*(cond_ProbSal[1][sal[:]==data[2]])
    print("\nProbability of being a junior:")
    print(prob_J)

    if prob_S>=prob_J:
        print("\nThe person in question is a Senior")
    else:
        print("\nThe person in question is a Junior")

dataset=[["senior", "sales", 31, 46],
    ["junior", "sales", 26, 26],
    ["junior", "sales", 31, 31],
    ["junior", "systems", 21, 46],
    ["senior", "systems", 31, 66],
    ["junior", "systems", 26, 46],
    ["senior", "systems", 41, 66],
    ["senior", "marketing", 36, 46],
    ["junior", "marketing", 31, 41],
    ["senior", "secretary", 46, 36],
    ["junior", "secretary", 26, 26]]

 

dataset = np.asarray(dataset)
features = dataset[:, 1:] #features
c_labels = dataset[:,0] #class labels

#Displaying the Data as well as various parameters

print("Attributes: \n", features) 
print("\nOutput: \n", c_labels)

prob_S, prob_J, cond_ProbDep, cond_ProbAge, cond_ProbSal = train(dataset)
input1 = ["sales", '31', '66']
print("\n\nThe prediction by Naive Bayes Classifier for ", input1 ," is:")
predict(input1, features, prob_S, prob_J, cond_ProbDep, cond_ProbAge, cond_ProbSal)
input = ["marketing", '31', '46']
print("\nThe prediction by Naive Bayes Classifier for ", input ," is:")
predict(input, features, prob_S, prob_J, cond_ProbDep, cond_ProbAge, cond_ProbSal)
