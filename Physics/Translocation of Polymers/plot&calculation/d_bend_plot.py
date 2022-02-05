import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# read in data from data.txt

with open ('d_bend_data.txt') as file_object :
    lines = file_object.readlines()
dataset = [[] for i in range(len(lines))]
for i in range(len(dataset)):
    dataset[i][:] = (item for item in lines[i].strip().split(' '))

# assign data to parameters

nsamp = int(dataset[0][0])
times = len(lines) - 2

cis_times = [0 for i in range(times)]
trans_times = [0 for i in range(times)]
cis_possibility = [0 for i in range(times)]
trans_possibility = [0 for i in range(times)]
avg_time = [0 for i in range(times)]
avg_cis_time = [0 for i in range(times)]
avg_trans_time = [0 for i in range(times)]
cis_Nsteps_left = [0 for i in range(times)]
cis_Nsteps_right = [0 for i in range(times)]
cis_Ntimes_left = [0 for i in range(times)]
cis_Ntimes_right = [0 for i in range(times)]
trans_Nsteps_left = [0 for i in range(times)]
trans_Nsteps_right = [0 for i in range(times)]
trans_Ntimes_left = [0 for i in range(times)]
trans_Ntimes_right = [0 for i in range(times)]
cis_left_times_steps = [0 for i in range(times)]
cis_right_times_steps = [0 for i in range(times)]
trans_left_times_steps = [0 for i in range(times)]
trans_right_times_steps = [0 for i in range(times)]
cis_left_times_minus_steps = [0 for i in range(times)]
cis_right_times_minus_steps = [0 for i in range(times)]
trans_left_times_minus_steps = [0 for i in range(times)]
trans_right_times_minus_steps = [0 for i in range(times)]
log_avg_time = [0 for i in range(times - 1)]
log_avg_cis_time = [0 for i in range(times - 1)]
log_avg_trans_time = [0 for i in range(times - 1)]
log_cis_Nsteps_left = [0 for i in range(times - 1)]
log_cis_Nsteps_right = [0 for i in range(times - 1)]
log_cis_Ntimes_left = [0 for i in range(times - 1)]
log_cis_Ntimes_right = [0 for i in range(times - 1)]
log_trans_Nsteps_left = [0 for i in range(times - 1)]
log_trans_Nsteps_right = [0 for i in range(times - 1)]
log_trans_Ntimes_left = [0 for i in range(times - 1)]
log_trans_Ntimes_right = [0 for i in range(times - 1)]
log_cis_left_times_steps = [0 for i in range(times - 1)]
log_cis_right_times_steps = [0 for i in range(times - 1)]
log_trans_left_times_steps = [0 for i in range(times - 1)]
log_trans_right_times_steps = [0 for i in range(times - 1)]
log_cis_left_times_minus_steps = [0 for i in range(times - 1)]
log_cis_right_times_minus_steps = [0 for i in range(times - 1)]
log_trans_left_times_minus_steps = [0 for i in range(times - 1)]
log_trans_right_times_minus_steps = [0 for i in range(times - 1)]

for i in range(times) :
    cis_times[i] = int(dataset[i + 2][0])
    trans_times[i] = int(dataset[i + 2][1])
    avg_cis_time[i] = float(dataset[i + 2][2])
    avg_trans_time[i] = float(dataset[i + 2][3])
    cis_Nsteps_left[i] = float(dataset[i + 2][4])
    cis_Nsteps_right[i] = float(dataset[i + 2][5])
    cis_Ntimes_left[i] = float(dataset[i + 2][6])
    cis_Ntimes_right[i] = float(dataset[i + 2][7])
    trans_Nsteps_left[i] = float(dataset[i + 2][8])
    trans_Nsteps_right[i] = float(dataset[i + 2][9])
    trans_Ntimes_left[i] = float(dataset[i + 2][10])
    trans_Ntimes_right[i] = float(dataset[i + 2][11])
    cis_left_times_steps[i] = cis_Ntimes_left[i] / cis_Nsteps_left[i]
    cis_right_times_steps[i] = cis_Ntimes_right[i] / cis_Nsteps_right[i]
    trans_left_times_steps[i] = trans_Ntimes_left[i] / trans_Nsteps_left[i]
    trans_right_times_steps[i] = trans_Ntimes_right[i] / trans_Nsteps_right[i]
    cis_left_times_minus_steps[i] = cis_Ntimes_left[i] - cis_Nsteps_left[i]
    cis_right_times_minus_steps[i] = cis_Ntimes_right[i] - cis_Nsteps_right[i]
    trans_left_times_minus_steps[i] = trans_Ntimes_left[i] - trans_Nsteps_left[i]
    trans_right_times_minus_steps[i] = trans_Ntimes_right[i] - trans_Nsteps_right[i]

for i in range(times - 1) :
    log_avg_cis_time[i] = avg_cis_time[i + 1]
    log_avg_trans_time[i] = avg_trans_time[i + 1]
    log_cis_Nsteps_left[i] = cis_Nsteps_left[i + 1]
    log_cis_Nsteps_right[i] = cis_Nsteps_right[i + 1]
    log_cis_Ntimes_left[i] = cis_Ntimes_left[i + 1]
    log_cis_Ntimes_right[i] = cis_Ntimes_right[i + 1]
    log_trans_Nsteps_left[i] = trans_Nsteps_left[i + 1]
    log_trans_Nsteps_right[i] = trans_Nsteps_right[i + 1]
    log_trans_Ntimes_left[i] = trans_Ntimes_left[i + 1]
    log_trans_Ntimes_right[i] = trans_Ntimes_right[i + 1]
    log_cis_left_times_steps[i] = cis_left_times_steps[i + 1]
    log_cis_right_times_steps[i] = cis_right_times_steps[i + 1]
    log_trans_left_times_steps[i] = trans_left_times_steps[i + 1]
    log_trans_right_times_steps[i] = trans_right_times_steps[i + 1]
    log_cis_left_times_minus_steps[i] = cis_left_times_minus_steps[i + 1]
    log_cis_right_times_minus_steps[i] = cis_right_times_minus_steps[i + 1]
    log_trans_left_times_minus_steps[i] = trans_left_times_minus_steps[i + 1]
    log_trans_right_times_minus_steps[i] = trans_right_times_minus_steps[i + 1]

# calculate possibility

for i in range(times) :
    cis_possibility[i] = cis_times[i] / nsamp
    trans_possibility[i] = trans_times[i] / nsamp

for i in range(times) :
    avg_time[i] = cis_possibility[i] * avg_cis_time[i] + trans_possibility[i] * avg_trans_time[i]

for i in range(times - 1) :
    log_avg_time[i] = avg_time[i + 1]

# assign x-axis: d_bend2

d_bend2 = [(0 * 1) for i in range(times)]
log_d_bend2 = [(0 * 1) for i in range(times - 1)]

for i in range(times):
    d_bend2[i] = int(dataset[1][i])

for i in range(times - 1) :
    log_d_bend2[i] = d_bend2[i + 1]

# plot possibility and average time curve

font1 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 40,
}
font2 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 30,
}
font3 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 35,
}
font4 = {'family' : 'Arial',
'weight' : 'normal',
'size'   : 25,
}

plt.figure()
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('p',font1)
plt.scatter(d_bend2,cis_possibility,80,'b')
plt.scatter(d_bend2,trans_possibility,80,'r')
plt.plot(d_bend2,cis_possibility,'b-',label=r'$p_{cis}$')
plt.plot(d_bend2,trans_possibility,'r--',label=r'$p_{trans}$')
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()

plt.figure()
plt.subplot(1,2,1)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel(r'$\tau$',font1)  
plt.title('(a)                                                      ',font1)  
plt.scatter(d_bend2,avg_cis_time,80,'b')
plt.scatter(d_bend2,avg_trans_time,80,'r')
plt.scatter(d_bend2,avg_time,20,'g')
plt.plot(d_bend2,avg_cis_time,'b-',label=r'$\tau_{cis}$')
plt.plot(d_bend2,avg_trans_time,'r--',label=r'$\tau_{trans}$')
plt.plot(d_bend2,avg_time,'g-.',label=r'$\tau$')
plt.legend(prop=font2)
plt.tick_params(labelsize=30)

plt.subplot(1,2,2)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel(r'$\tau$',font1)
plt.title('(b)                                                     ',font1)  
plt.scatter(log_d_bend2,log_avg_cis_time,80,'b')
plt.scatter(log_d_bend2,log_avg_trans_time,80,'r')
plt.scatter(log_d_bend2,log_avg_time,80,'g')
plt.loglog(log_d_bend2,log_avg_cis_time,'b-',label=r'$\tau_{cis}$')
plt.loglog(log_d_bend2,log_avg_trans_time,'r--',label=r'$\tau_{trans}$')
plt.loglog(log_d_bend2,log_avg_time,'g-.',label=r'$\tau$')
plt.xlim(left=0.9)
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()

total_slope = 0
cis_slope = 0
trans_slope =0
for i in range(times - 3) :
    total_slope = total_slope + (math.log(log_avg_time[i + 1]) - math.log(log_avg_time[i])) / (math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    cis_slope = cis_slope + (math.log(log_avg_cis_time[i + 1]) - math.log(log_avg_cis_time[i])) / (math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    trans_slope = trans_slope + (math.log(log_avg_trans_time[i + 1]) - math.log(log_avg_trans_time[i])) / (math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)

print('total_slope = ',total_slope,', cis_slope = ',cis_slope,', trans_slope = ',trans_slope)

plt.figure()
plt.subplot(1,2,1)
plt.xlabel(r'$k_\theta$',font3)
plt.ylabel('t',font3)
plt.title('(a)                                                      ',font1) 
plt.scatter(d_bend2,cis_Nsteps_left,80,'b')
plt.scatter(d_bend2,cis_Nsteps_right,80,'r')
plt.scatter(d_bend2,cis_Ntimes_left,80,'g')
plt.scatter(d_bend2,cis_Ntimes_right,80,'m')
plt.plot(d_bend2,cis_Nsteps_left,'b-',label=r'$s_{cis}$')
plt.plot(d_bend2,cis_Nsteps_right,'r--',label=r'$s_{trans}$')
plt.plot(d_bend2,cis_Ntimes_left,'g-.',label=r'$t_{cis}$')
plt.plot(d_bend2,cis_Ntimes_right,'m:',label=r'$t_{trans}$')
plt.legend(prop=font4)
plt.tick_params(labelsize=20)

plt.subplot(1,2,2)
plt.xlabel(r'$k_\theta$',font3)
plt.ylabel('t',font3)
plt.title('(b)                                                      ',font1) 
plt.scatter(d_bend2,trans_Nsteps_left,80,'b')
plt.scatter(d_bend2,trans_Nsteps_right,80,'r')
plt.scatter(d_bend2,trans_Ntimes_left,80,'g')
plt.scatter(d_bend2,trans_Ntimes_right,80,'m')
plt.plot(d_bend2,trans_Nsteps_left,'b-',label=r'$s_{cis}$')
plt.plot(d_bend2,trans_Nsteps_right,'r--',label=r'$s_{trans}$')
plt.plot(d_bend2,trans_Ntimes_left,'g-.',label=r'$t_{cis}$')
plt.plot(d_bend2,trans_Ntimes_right,'m:',label=r'$t_{trans}$')
plt.legend(prop=font4)
plt.tick_params(labelsize=20)
plt.show()

plt.figure()
plt.subplot(1,2,1)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('t',font1)
plt.title('(a)                                                      ',font1) 
plt.scatter(log_d_bend2,log_cis_Nsteps_left,80,'b')
plt.scatter(log_d_bend2,log_cis_Nsteps_right,80,'r')
plt.scatter(log_d_bend2,log_cis_Ntimes_left,80,'g')
plt.scatter(log_d_bend2,log_cis_Ntimes_right,80,'m')
plt.loglog(log_d_bend2,log_cis_Nsteps_left,'b-',label=r'$s_{cis}$')
plt.loglog(log_d_bend2,log_cis_Nsteps_right,'r--',label=r'$s_{trans}$')
plt.loglog(log_d_bend2,log_cis_Ntimes_left,'g-.',label=r'$t_{cis}$')
plt.loglog(log_d_bend2,log_cis_Ntimes_right,'m:',label=r'$t_{trans}$')
plt.xlim(left=0.9)
plt.legend(prop=font4)
plt.tick_params(labelsize=30)

cis_steps_left_slope = 0
cis_steps_right_slope = 0
cis_time_left_slope = 0
cis_time_right_slope = 0
for i in range(times - 3) :
    cis_steps_left_slope = cis_steps_left_slope + (math.log(log_cis_Nsteps_left[i + 1]) - math.log(log_cis_Nsteps_left[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    cis_steps_right_slope = cis_steps_right_slope + (math.log(log_cis_Nsteps_right[i + 1]) - math.log(log_cis_Nsteps_right[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    cis_time_left_slope = cis_time_left_slope + (math.log(log_cis_Ntimes_left[i + 1]) - math.log(log_cis_Ntimes_left[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    cis_time_right_slope = cis_time_right_slope + (math.log(log_cis_Ntimes_right[i + 1]) - math.log(log_cis_Ntimes_right[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)

print('cis_steps_left_slope = ',cis_steps_left_slope,', cis_steps_right_slope = ',cis_steps_right_slope,', cis_time_left_slop = ',cis_time_left_slope,', cis_time_right_slope = ',cis_time_right_slope)

plt.subplot(1,2,2)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('t',font1)
plt.title('(b)                                                      ',font1) 
plt.scatter(log_d_bend2,log_trans_Nsteps_left,80,'b')
plt.scatter(log_d_bend2,log_trans_Nsteps_right,80,'r')
plt.scatter(log_d_bend2,log_trans_Ntimes_left,80,'g')
plt.scatter(log_d_bend2,log_trans_Ntimes_right,80,'m')
plt.loglog(log_d_bend2,log_trans_Nsteps_left,'b-',label=r'$s_{cis}$')
plt.loglog(log_d_bend2,log_trans_Nsteps_right,'r--',label=r'$s_{trans}$')
plt.loglog(log_d_bend2,log_trans_Ntimes_left,'g-.',label=r'$t_{cis}$')
plt.loglog(log_d_bend2,log_trans_Ntimes_right,'m:',label=r'$t_{trans}$')
plt.xlim(left=0.9)
plt.legend(prop=font4)
plt.tick_params(labelsize=26)
plt.show()

trans_steps_left_slope = 0
trans_steps_right_slope = 0
trans_time_left_slope = 0
trans_time_right_slope = 0
for i in range(times - 3) :
    trans_steps_left_slope = trans_steps_left_slope + (math.log(log_trans_Nsteps_left[i + 1]) - math.log(log_trans_Nsteps_left[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    trans_steps_right_slope = trans_steps_right_slope + (math.log(log_trans_Nsteps_right[i + 1]) - math.log(log_trans_Nsteps_right[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    trans_time_left_slope = trans_time_left_slope + (math.log(log_trans_Ntimes_left[i + 1]) - math.log(log_trans_Ntimes_left[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)
    trans_time_right_slope = trans_time_right_slope + (math.log(log_trans_Ntimes_right[i + 1]) - math.log(log_trans_Ntimes_right[i]))/(math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i]))/(times - 2)

print('trans_steps_left_slope = ',trans_steps_left_slope,', trans_steps_right_slope = ',trans_steps_right_slope,', trans_time_left_slop = ',trans_time_left_slope,', trans_time_right_slope = ',trans_time_right_slope)

plt.figure()
plt.subplot(1,2,1)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('time per step',font1)
plt.scatter(d_bend2,cis_left_times_steps,20,'b')
plt.scatter(d_bend2,cis_right_times_steps,20,'r')
plt.plot(d_bend2,cis_left_times_steps,'b-',label='<'r'$t/steps_{escape}$''>_left')
plt.plot(d_bend2,cis_right_times_steps,'r--',label='<'r'$t/steps_{escape}$''>_right')
plt.legend(prop=font2)
plt.tick_params(labelsize=30)

plt.subplot(1,2,2)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('time per step',font1)
plt.scatter(d_bend2,trans_left_times_steps,20,'b')
plt.scatter(d_bend2,trans_right_times_steps,20,'r')
plt.plot(d_bend2,trans_left_times_steps,'b-',label='<'r'$t/steps_{escape}$''>_left')
plt.plot(d_bend2,trans_right_times_steps,'r--',label='<'r'$t/steps_{escape}$''>_right')
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()

plt.figure()
plt.subplot(1,2,1)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('time per step',font1)
plt.scatter(log_d_bend2,log_cis_left_times_steps,20,'b')
plt.scatter(log_d_bend2,log_cis_right_times_steps,20,'r')
plt.loglog(log_d_bend2,log_cis_left_times_steps,'b-',label='<'r'$t/steps_{escape}$''>_left')
plt.loglog(log_d_bend2,log_cis_right_times_steps,'r--',label='<'r'$t/steps_{escape}$''>_right')
plt.xlim(left=0.9)
plt.legend(prop=font2)
plt.tick_params(labelsize=30)

plt.subplot(1,2,2)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('time per step',font1)
plt.scatter(log_d_bend2,log_trans_left_times_steps,20,'b')
plt.scatter(log_d_bend2,log_trans_right_times_steps,20,'r')
plt.loglog(log_d_bend2,log_trans_left_times_steps,'b-',label='<'r'$t/steps_{escape}$''>_left')
plt.loglog(log_d_bend2,log_trans_right_times_steps,'r--',label='<'r'$t/steps_{escape}$''>_right')
plt.xlim(left=0.9)
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()

cis_left_slope = 0
cis_right_slope = 0
trans_left_slope = 0
trans_right_slope = 0
for i in range(times - 3) :
    cis_left_slope = cis_left_slope + (math.log(log_cis_left_times_steps[i + 1]) - math.log(log_cis_left_times_steps[i])) / (math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i])) / (times - 2)
    cis_right_slope = cis_right_slope + (math.log(log_cis_right_times_steps[i + 1]) - math.log(log_cis_right_times_steps[i])) / (math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i])) / (times - 2)
    trans_left_slope = trans_left_slope + (math.log(log_trans_left_times_steps[i + 1]) - math.log(log_trans_left_times_steps[i])) / (math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i])) / (times - 2)
    trans_right_slope = trans_right_slope + (math.log(log_trans_right_times_steps[i + 1]) - math.log(log_trans_right_times_steps[i])) / (math.log(log_d_bend2[i + 1]) - math.log(log_d_bend2[i])) / (times - 2)

print('cis_left_slope = ',cis_left_slope,'cis_right_slope = ',cis_right_slope,'trans_left_slope = ',trans_left_slope,'trans_right_slope = ',trans_right_slope)

plt.figure()
plt.subplot(1,2,1)
plt.xlabel(r'$k_\theta$',font3)
plt.ylabel('time-step',font3)
plt.scatter(d_bend2,cis_left_times_minus_steps,20,'b')
plt.scatter(d_bend2,cis_right_times_minus_steps,20,'r')
plt.plot(d_bend2,cis_left_times_minus_steps,'b-',label='<'r'$t-steps_{escape}$''>_left')
plt.plot(d_bend2,cis_right_times_minus_steps,'r--',label='<'r'$t-steps_{escape}$''>_right')
plt.legend(prop=font2)
plt.tick_params(labelsize=20)

plt.subplot(1,2,2)
plt.xlabel(r'$k_\theta$',font3)
plt.ylabel('time-step',font3)
plt.scatter(d_bend2,trans_left_times_minus_steps,20,'b')
plt.scatter(d_bend2,trans_right_times_minus_steps,20,'r')
plt.plot(d_bend2,trans_left_times_minus_steps,'b-',label='<'r'$t-steps_{escape}$''>_left')
plt.plot(d_bend2,trans_right_times_minus_steps,'r--',label='<'r'$t-steps_{escape}$''>_right')
plt.legend(prop=font2)
plt.tick_params(labelsize=20)
plt.show()

plt.figure()
plt.subplot(1,2,1)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('time-step',font1)
plt.scatter(log_d_bend2,log_cis_left_times_minus_steps,20,'b')
plt.scatter(log_d_bend2,log_cis_right_times_minus_steps,20,'r')
plt.loglog(log_d_bend2,log_cis_left_times_minus_steps,'b-',label='<'r'$t-steps_{escape}$''>_left')
plt.loglog(log_d_bend2,log_cis_right_times_minus_steps,'r--',label='<'r'$t-steps_{escape}$''>_right')
plt.xlim(left=0.9)
plt.legend(prop=font2)
plt.tick_params(labelsize=30)

plt.subplot(1,2,2)
plt.xlabel(r'$k_\theta$',font1)
plt.ylabel('time-step',font1)
plt.scatter(log_d_bend2,log_trans_left_times_minus_steps,20,'b')
plt.scatter(log_d_bend2,log_trans_right_times_minus_steps,20,'r')
plt.loglog(log_d_bend2,log_trans_left_times_minus_steps,'b-',label='<'r'$t-steps_{escape}$''>_left')
plt.loglog(log_d_bend2,log_trans_right_times_minus_steps,'r--',label='<'r'$t-steps_{escape}$''>_right')
plt.xlim(left=0.9)
plt.legend(prop=font2)
plt.tick_params(labelsize=30)
plt.show()