import sys
sys.setrecursionlimit(1000000000)

import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# define functions

def C3(Nleft,Nright,Nstill,p_left,p_right,p_still) :
    if Nleft == 1 and Nright == 1 and Nstill == 1 :
        return 6 * p_left * p_right * p_still
    elif Nleft > 1 :
        return (Nleft + Nright + Nstill) * p_left / Nleft * C3(Nleft - 1,Nright,Nstill,p_left,p_right,p_still)
    elif Nright > 1 :
        return (Nleft + Nright + Nstill) * p_right / Nright * C3(Nleft,Nright - 1,Nstill,p_left,p_right,p_still)
    elif Nstill > 1 :
        return (Nleft + Nright + Nstill) * p_still / Nstill * C3(Nleft,Nright,Nstill - 1,p_left,p_right,p_still)
    else :
        print('error')

# read in Nstep stats

with open ('Nstep_data.txt') as file_object :
    N_lines = file_object.readlines()

N0_dataset = [[] for i in range(len(N_lines))]
N_dataset = [[] for i in range(len(N_lines))]

for i in range(len(N_lines)) :
    N0_dataset[i][:] = (item for item in N_lines[i].strip().split(' '))

for i in range(len(N_lines)) :
    for j in range(len(N0_dataset[i])) :
        if N0_dataset[i][j] == '' :
            continue
        else :
            N_dataset[i].append(N0_dataset[i][j])

sample = len(N_lines) - 1

Steps = [0 for i in range(sample)]
Nleft = [0 for i in range(sample)]
Nright = [0 for i in range(sample)]
Nstill = [0 for i in range(sample)]

for i in range(sample) :
    Steps[i] = int(float(N_dataset[i + 1][1]))
    Nleft[i] = int(N_dataset[i + 1][2])
    Nright[i] = int(N_dataset[i + 1][3])
    Nstill[i] = Steps[i] - Nleft[i] - Nright[i]

# determine p stats

d_bend2 = int(N_dataset[0][0])

p_left = [0 for i in range(sample)]
p_right = [0 for i in range(sample)]
p_still = [0 for i in range(sample)]

for i in range(sample) :
    p_left[i] = Nleft[i] / Steps[i]
    p_right[i] = Nright[i] / Steps[i]
    p_still[i] = 1 - p_left[i] - p_right[i]

# calculate escape possibility

totalcispo = 0
totaltranspo = 0
cistime = 0
transtime = 0

for i in range(sample) :
    if Nleft[i] > Nright[i] :
        totalcispo = totalcispo + C3(Nleft[i],Nright[i],Nstill[i],p_left[i],p_right[i],p_still[i])
        cistime = cistime + 1
    else :
        totaltranspo = totaltranspo + C3(Nleft[i],Nright[i],Nstill[i],p_left[i],p_right[i],p_still[i])
        transtime = transtime + 1

cispossibility = totalcispo / cistime
transpossibility = totaltranspo / transtime

print(cispossibility,transpossibility)