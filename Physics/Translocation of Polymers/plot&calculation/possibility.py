import sys
sys.setrecursionlimit(1000000000)

import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# define functions

def C2(Nleft,Nright,p) :
    if Nleft == 1 and Nright == 1 :
        return 2 * p * (1 - p)
    elif Nleft > 1 :
        return (Nleft + Nright) * (1 - p) / Nleft * C2(Nleft - 1,Nright,p)
    elif Nright > 1 :
        return (Nleft + Nright) * p / Nright * C2(Nleft,Nright - 1,p)
    else :
        print('error')

# read in p stats
        
with open ('p_data.txt') as file_object :
    p_lines = file_object.readlines()

p_dataset = [[] for i in range(len(p_lines))]

for i in range(len(p_lines)):
    p_dataset[i][:] = (item for item in p_lines[i].strip().split(' '))


d_bend2_set = [0 for i in range(len(p_lines))]
p_set = [0 for i in range(len(p_lines))]

for i in range(len(p_lines)) :
    d_bend2_set[i] = int(p_dataset[i][0])
    p_set[i] = float(p_dataset[i][1])

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

Nleft = [0 for i in range(sample)]
Nright = [0 for i in range(sample)]

for i in range(sample) :
    Nleft[i] = int(N_dataset[i + 1][2])
    Nright[i] = int(N_dataset[i + 1][3])

# determine p stats

d_bend2 = int(N_dataset[0][0])

if d_bend2 <= 10 :
    p = p_set[d_bend2]
elif d_bend2 % 5 == 0 :
    p = p_set[int(10 + (d_bend2 - 10) / 5)]
else :
    print('d_bend2 input error')

# calculate escape possibility

totalpo = 0

for i in range(sample) :
    totalpo = totalpo + C2(Nleft[i],Nright[i],p)

possibility = totalpo / sample

print(possibility)