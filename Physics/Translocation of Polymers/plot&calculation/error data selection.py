import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# read in Nstep stats

with open ('error data.txt') as file_object :
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

sample = 1000

time = [0 for i in range(sample)]
left_steps = [0 for i in range(sample)]
right_steps = [0 for i in range(sample)]
left_time = [0 for i in range(sample)]
right_time = [0 for i in range(sample)]
escape_direction = [0 for i in range(sample)]

for i in range(sample) :
    time[i] = int(float(dataset[i + 1000][1]))
    left_steps[i] = int(dataset[i + 1000][2])
    right_steps[i] = int(dataset[i + 1000][3])
    left_time[i] = int(dataset[i + 1000][4])
    right_time[i] = int(dataset[i + 1000][5])
    escape_direction[i] = int(dataset[i + 1000][6])

#calculate stats

cis_times = 0
trans_times = 0
sum_cis_time = 0
sum_trans_time = 0
sum_cis_left_steps = 0
sum_cis_right_steps = 0
sum_cis_left_time = 0
sum_cis_right_time = 0
sum_trans_left_steps = 0
sum_trans_right_steps = 0
sum_trans_left_time = 0
sum_trans_right_time = 0

for i in range(sample) :
    if escape_direction[i] == 1 :
        cis_times = cis_times + 1
        sum_cis_time = sum_cis_time + time[i]
        sum_cis_left_steps = sum_cis_left_steps + left_steps[i]
        sum_cis_right_steps = sum_cis_right_steps + right_steps[i]
        sum_cis_left_time = sum_cis_left_time + left_time[i]
        sum_cis_right_time = sum_cis_right_time + right_time[i]
    else :
        trans_times = trans_times + 1
        sum_trans_time = sum_trans_time + time[i]
        sum_trans_left_steps = sum_trans_left_steps + left_steps[i]
        sum_trans_right_steps = sum_trans_right_steps + right_steps[i]
        sum_trans_left_time = sum_trans_left_time + left_time[i]
        sum_trans_right_time = sum_trans_right_time + right_time[i]

print(cis_times,trans_times,round(sum_cis_time/cis_times,2),round(sum_trans_time/trans_times,2),round(sum_cis_left_steps/cis_times,2),round(sum_cis_right_steps/cis_times,2),round(sum_cis_left_time/cis_times,2),round(sum_cis_right_time/cis_times,2),round(sum_trans_left_steps/trans_times,2),round(sum_trans_right_steps/trans_times,2),round(sum_trans_left_time/trans_times,2),round(sum_trans_right_time/trans_times,2))