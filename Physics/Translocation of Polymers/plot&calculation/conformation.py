import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

# read in data from data.txt

with open ('ini_conf.txt') as file_object :
    lines = file_object.readlines()

dataset0 = [[] for i in range(len(lines))]
dataset = [[] for i in range(len(lines))]

for i in range(len(lines)) :
    dataset0[i][:] = (item for item in lines[i].strip().split(' '))

for i in range(len(lines)) :
    for j in range(len(dataset0[i])) :
        if dataset0[i][j] == '' :
            continue
        else :
            dataset[i].append(dataset0[i][j])

monomers = 65
x = [0 for i in range(monomers)]
z = [0 for i in range(monomers)]

for i in range(monomers) :
    x[i] = float(dataset[i + 1][0])
    z[i] = float(dataset[i + 1][2])

wall1 = [100,100]
wall2 = [0,39]
wall3 = [100,100]
wall4 = [41,80]

font1 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 40,
}
font2 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 20,
}

plt.figure()
plt.scatter(x,z,20,'r')
plt.plot(x,z,'r')
plt.plot(wall1,wall2,linewidth=4,color='blue')
plt.plot(wall3,wall4,linewidth=4,color='blue')
plt.text(83,55,"cis space",font1)
plt.text(108,55,"trans space",font1)
ax=plt.gca()
plt.axis([75,125,15,65])
plt.xticks([])
plt.yticks([])
plt.show()