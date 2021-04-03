import numpy as np
import pandas as pd
from numpy import log2 as log
import pprint
eps = np.finfo(float).eps
#Training Code for Task 1

def find_ent(df):
    attr = df.keys()[-1]   #changing target variable class name
    ent = 0
    values = df[attr].unique()
    for value in values:
        fraction = df[attr].value_counts()[value]/len(df[attr])
        ent += -fraction*np.log2(fraction)
    return ent
  
  
def find_ent_attr(df,attr):
  attr = df.keys()[-1]   # changing target variable name
  target_var = df[attr].unique()  #This gives all 'Yes' and 'No'
  var_values = df[attr].unique()    #This gives different features in that attributes (like 'Hot','Cold' in Temperature)
  ent2 = 0
  for values in var_values:
      ent = 0
      for target_variable in target_var:
          num = len(df[attr][df[attr]==values][df[attr] ==target_variable])
          den = len(df[attr][df[attr]==values])
          fraction = num/(den+eps)
          ent += -fraction*log(fraction+eps)
      fraction2 = den/len(df)
      ent2 += -fraction2*ent
  return abs(ent2)

def find_winner(df):
    ent_att = []
    IG = []
    for key in df.keys()[:-1]:
        IG.append(find_ent(df)-find_ent_attr(df,key))
    return df.keys()[:-1][np.argmax(IG)]
  
  
def get_subtable(df, node,value):
  return df[df[node] == value].reset_index(drop=True)

# Building our decision tree
def buildTree(df, attr, tree=None): 
    attr = df.keys()[-1]   
    node = find_winner(df)
    
    #Get distinct value of that attr e.g Salary is node and Low,Med and High are values
    attValue = np.unique(df[node])
    
    #Create an empty dictionary to create tree    
    if tree is None:                    
        tree={}
        tree[node] = {}
    
   #We make loop to construct a tree by calling this function recursively.  
    for value in attValue:
        
        subtable = get_subtable(df,node,value)
        clValue,counts = np.unique(subtable[attr],return_counts=True)                        
        
        if len(counts)==1: #Checking purity of subset
            tree[node][value] = clValue[0]                                                    
        else:        
            tree[node][value] = buildTree(subtable,attr) #Calling the function recursively 
                   
    return tree

def predict(inst,tree):
    #This function is used to predict for any input values 
    #Recursively we go through the tree that we built earlier

    for nodes in tree.keys():        
        
        value = inst[nodes]
        tree = tree[nodes][value]
        prediction = 0
            
        if type(tree) is dict:
            prediction = predict(inst, tree)
        else:
            prediction = tree
            break;                            
        
    return prediction

if __name__== "__main__": 
  #First Training the tuplesets
  #Task 1 tupleset
  tupleset = {'Outlook':['Rainy','Rainy','Overcast','Sunny','Sunny','Sunny','Overcast','Rainy','Rainy','Sunny','Rainy','Overcast','Overcast','Sunny'],
        'Temperature':['Hot','Hot','Hot','Mild','Cool','Cool','Cool','Mild','Cool','Mild','Mild','Mild','Hot','Mild'],
        'Humidity':['High','High','High','High','Normal','Normal','Normal','High','Normal','Normal','Normal','High','Normal','High'],
        'Windy':['FALSE','TRUE','FALSE','FALSE','FALSE','TRUE','TRUE','FALSE','FALSE','FALSE','TRUE','TRUE','FALSE','TRUE'],
        'PlayGolf':['No','No','Yes','Yes','Yes','No','Yes','No','Yes','Yes','Yes','Yes','Yes','No']}

  df = pd.tupleFrame(tupleset,columns=['Outlook','Temperature','Humidity','Windy','PlayGolf'])#storing labels of tuple so that we can use specific tuple...
  ent_node = 0  #Initialize ent
  values = df.PlayGolf.unique()  #Unique objects - 'Yes', 'No'
  for value in values:
      fraction = df.PlayGolf.value_counts()[value]/len(df.PlayGolf)  
      ent_node += -fraction*np.log2(fraction)

  attr = 'PlayGolf'
  target_var = df.PlayGolf.unique()  #This gives all 'Yes' and 'No'
  var_values = df[attr].unique()    #This gives different features in that attr
  ent_attr = 0
  for values in var_values:
      ent_each_feature = 0
      for target_variable in target_var:
          num = len(df[attr][df[attr]==values][df.PlayGolf ==target_variable]) #numerator
          den = len(df[attr][df[attr]==values])  #denominator
          fraction = num/(den+eps)  #pi
          ent_each_feature += -fraction*log(fraction+eps) #This calculates ent for one feature
      fraction2 = den/len(df)
