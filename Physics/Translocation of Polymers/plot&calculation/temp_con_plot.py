import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# read in data from data.txt

with open ('temp_con_data.txt') as file_object :
    lines = file_object.readlines()
dataset = [[] for i in range(len(lines))]
for i in range(len(dataset)):
    dataset[i][:] = (item for item in lines[i].strip().split(' '))

# assign data to parameters

times = len(lines) - 1

ini_cis = [0 for i in range(times)]
ini_trans = [0 for i in range(times)]
ini_total = [0 for i in range(times)]
fin_cis = [0 for i in range(times - 1)]
fin_trans = [0 for i in range(times - 3)]

for i in range(times) :
    ini_cis[i] = float(dataset[i + 1][0])
    ini_trans[i] = float(dataset[i + 1][1])
    ini_total[i] = float(dataset[i + 1][2])

# assign x-axis: d_bend

temp = [(0 * 1) for i in range(times)]
tempcis = [0 for i in range(times - 1)]
temptrans = [0 for i in range(times - 3)]

for i in range(times) :
    temp[i] = float(dataset[0][i])

for i in range(times - 1) :
    tempcis[i] = float(dataset[0][i])
    fin_cis[i] = float(dataset[i + 1][3])

for i in range(times - 3) :
    temptrans[i] = float(dataset[0][i + 3])
    fin_trans[i] = float(dataset[i + 4][4])

# plot conformation curve

font1 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 40,
}
font2 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 25,
}

plt.figure()
plt.xlabel('T',font1)
plt.ylabel(r'$R^{half}$',font1)
plt.scatter(temp,ini_cis,80,'b')
plt.scatter(temp,ini_trans,80,'r')
plt.plot(temp,ini_cis,'b-',label=r'$R_{cis}^{half}$')
plt.plot(temp,ini_trans,'r--',label=r'$R_{trans}^{half}$')
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()

plt.figure()
plt.xlabel('T',font1)
plt.ylabel('R',font1)
plt.scatter(tempcis,fin_cis,80,'b')
plt.scatter(temptrans,fin_trans,80,'r')
plt.scatter(temp,ini_total,80,'g')
plt.plot(tempcis,fin_cis,'b-',label=r'$R_{cis}$')
plt.plot(temptrans,fin_trans,'r--',label=r'$R_{trans}$')
plt.plot(temp,ini_total,'g-.',label=r'$R_{ini}$')
plt.ylim(5,15)
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()