import pandas as pd
import numpy as np
from math import sqrt
import operator

x1 = np.array([0,0,1,1])
x2 = np.array([0,1,0,1])

z1 = x1 - x2
z2 = x2 - x1
a1 = np.array([1 if  i >= 1 else 0 for i in z1])
a2 = np.array([1 if  i >= 1 else 0 for i in z2])

z3 = a1 + a2
a3 = [1 if  i >= 1 else 0 for i in z3]

print("XOR Output:", a3)
