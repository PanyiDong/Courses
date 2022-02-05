import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# read in data from data.txt

with open ('eta_con_data.txt') as file_object :
    lines = file_object.readlines()
dataset = [[] for i in range(len(lines))]
for i in range(len(dataset)):
    dataset[i][:] = (item for item in lines[i].strip().split(' '))

# assign data to parameters

times = len(lines) - 1

ini_cis = [0 for i in range(times)]
ini_trans = [0 for i in range(times)]
ini_total = [0 for i in range(times)]
fin_cis = [0 for i in range(times - 2)]
fin_trans = [0 for i in range(times - 1)]

for i in range(times) :
    ini_cis[i] = float(dataset[i + 1][0])
    ini_trans[i] = float(dataset[i + 1][1])
    ini_total[i] = float(dataset[i + 1][2])

# assign x-axis: d_bend

eta = [0 for i in range(times)]
etacis = [0 for i in range(times - 2)]
etatrans = [0 for i in range(times - 1)]

for i in range(times) :
    eta[i] = float(dataset[0][i])

for i in range(times - 2) :
    etacis[i] = float(dataset[0][i + 2])
    fin_cis[i] = float(dataset[i + 3][3])

for i in range(times - 1) :
    etatrans[i] = float(dataset[0][i])
    fin_trans[i] = float(dataset[i + 1][4])

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
plt.xlabel(r'$\eta$',font1)
plt.ylabel(r'$R^{half}$',font1)
plt.scatter(eta,ini_cis,80,'b')
plt.scatter(eta,ini_trans,80,'r')
plt.plot(eta,ini_cis,'b-',label=r'$R_{cis}^{half}$')
plt.plot(eta,ini_trans,'r--',label=r'$R_{trans}^{half}$')
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()

plt.figure()
plt.xlabel(r'$\eta$',font1)
plt.ylabel('R',font1)
plt.scatter(etacis,fin_cis,80,'b')
plt.scatter(etatrans,fin_trans,80,'r')
plt.scatter(eta,ini_total,80,'g')
plt.plot(etacis,fin_cis,'b-',label=r'$R_{cis}$')
plt.plot(etatrans,fin_trans,'r--',label=r'$R_{trans}$')
plt.plot(eta,ini_total,'g-.',label=r'$R_{ini}$')
plt.ylim(5,15)
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()