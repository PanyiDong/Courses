#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#规定常数,position0为初始粒子分布（不发生变化），position1为区域边界下的位置，posiion2为全局位置
sigma = 0.1
meanR = 1
Number = 2000
length = 200
K = 10
cellsize = length/K
dlumda = 0.02
stime = 10000
position0 = [([0] * 2) for i in range(Number)]
position1 = [([0] * 2) for i in range(3*Number)]
position2 = [([0] * 2) for i in range(3*Number)]
R=[(0 * 1) for i in range(3*Number)]
MSD=[(0 * 1) for i in range(stime)]
time=[(0 * 1) for i in range(stime)]
lMSD=[(0 * 1) for i in range(stime)]
ltime=[(0 * 1) for i in range(stime)]

#定义空白cell list区域并写出规划粒子的函数
cell0 = []
rows = K+2
columns = K+2
for row in range(rows):
    cell0.append([])
    for column in range(columns):
        cell0[row].append([])

def cellist0(position0,i):
    return [int(position0[i][0]//cellsize+1),int(position0[i][1]//cellsize+1)]

def cellist1(position0,i):
    return [int(position1[i][0]//cellsize+1),int(position1[i][1]//cellsize+1)]

#生成满足正态分布的粒子半径并去除不需要的部分
i = 0
random.seed(Number)
while i<Number:
    R[i] = random.gauss(meanR, sigma)
    if abs(R[i]-1)-3*sigma>0:
        i = i-1
    i = i+1   

#算出粒子的体积分数
V = 0
j = 0
for j in range(Number):
    V = V+math.pi*R[j]**2
Phi = V/length**2
print('粒子的体积分数为%.2f' % Phi)

#随机生成粒子位置并列入list中
i = 0
position0[0][0] = random.random()*length
position0[0][1] = random.random()*length
cell0[int(position0[i][0]//cellsize+1)][int(position0[i][1]//cellsize+1)].append(i)
i=1
while i<Number:
    cellroom = [0,0]
    position0[i][0] = random.uniform(0,length)
    position0[i][1] = random.uniform(0,length)
    cellroom = cellist0(position0,i)
    m = 1
    if cellroom[0] == 1:
        if cellroom[1] == 1:
            for j in cell0[1][1]+cell0[2][1]+cell0[1][2]+cell0[2][2]:
                if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                    m = 0
                    continue
        elif cellroom[1] == K:
            for j in cell0[1][K]+cell0[1][K-1]+cell0[2][K]+cell0[2][K-1]:
                if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                    m = 0
                    continue
        else:
            for j in cell0[1][cellroom[1]]+cell0[1][cellroom[1]-1]+cell0[1][cellroom[1]+1]+cell0[2][cellroom[1]]+cell0[2][cellroom[1]-1]+cell0[2][cellroom[1]+1]:
                if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                    m = 0
                    continue
    elif cellroom[0] == K:
        if cellroom[1] == 1:
            for j in cell0[K][1]+cell0[K-1][1]+cell0[K][2]+cell0[K-1][2]:
                if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                    m = 0
                    continue
        elif cellroom[1] == K:
            for j in cell0[K][K]+cell0[K-1][K]+cell0[K][K-1]+cell0[K-1][K-1]:
                if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                    m = 0
                    continue
        else:
            for j in cell0[K][cellroom[1]]+cell0[K][cellroom[1]-1]+cell0[K][cellroom[1]+1]+cell0[K-1][cellroom[1]]+cell0[K-1][cellroom[1]-1]+cell0[K-1][cellroom[1]+1]:
                if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                    m = 0
                    continue
    elif cellroom[1] == 1:
        for j in cell0[cellroom[0]][1]+cell0[cellroom[0]-1][1]+cell0[cellroom[0]+1][1]+cell0[cellroom[0]][2]+cell0[cellroom[0]+1][2]+cell0[cellroom[0]-1][2]:
            if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                m = 0
                continue
    elif cellroom[1] == K:
        for j in cell0[cellroom[0]][K]+cell0[cellroom[0]-1][K]+cell0[cellroom[0]+1][K]+cell0[cellroom[0]][K-1]+cell0[cellroom[0]-1][K-1]+cell0[cellroom[0]+1][K-1]:
            if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                m = 0
                continue
    else:
        for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]][cellroom[1]+1]+cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]-1]+cell0[cellroom[0]-1][cellroom[1]+1] \
        +cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]-1]+cell0[cellroom[0]+1][cellroom[1]+1]:
            if (i != j) & ((position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0):
                m = 0
                continue
    if m == 1:
        cell0[int(position0[i][0]//cellsize+1)][int(position0[i][1]//cellsize+1)].append(i)
        i=i+1

#将初始粒子分布分配到position1,position2
for i in range(Number):
    position1[i][0] = position0[i][0]
    position1[i][1] = position0[i][1]
    position2[i][0] = position0[i][0]
    position2[i][1] = position0[i][1]

#模拟粒子运动
for t in range(stime):
    MSD[t] = 0
    time[t] = t+1
    for ts in range(100):
        movement = [0,0]
        chosen = random.randint(0,Number-1)
        movement[0] = 2*dlumda*random.random()-dlumda
        movement[1] = 2*dlumda*random.random()-dlumda
        originx1 = position1[chosen][0]
        originy1 = position1[chosen][1]
        originx2 = position2[chosen][0]
        originy2 = position2[chosen][1]
        cell0[int(position1[chosen][0]//cellsize+1)][int(position1[chosen][1]//cellsize+1)].remove(chosen)

        #防止粒子在周期性条件下运动后超出范围,position2无需考虑
        if position1[chosen][0]+movement[0]<0:
            position1[chosen][0] = position1[chosen][0]+length
        elif position1[chosen][0]+movement[0]>length:
            position1[chosen][0] = position1[chosen][0]-length
        if position1[chosen][1]+movement[1]<0:
            position1[chosen][1] = position1[chosen][1]+length
        elif position1[chosen][1]+movement[1]>length:
            position1[chosen][1] = position1[chosen][1]-length
        
        position1[chosen][0] = position1[chosen][0]+movement[0]
        position1[chosen][1] = position1[chosen][1]+movement[1]
        position2[chosen][0] = position2[chosen][0]+movement[0]
        position2[chosen][1] = position2[chosen][1]+movement[1]
        cell0[int(position1[chosen][0]//cellsize+1)][int(position1[chosen][1]//cellsize+1)].append(chosen)
        cellroom = cellist1(position1,chosen)

        #在给定体积周围增加一圈，构造周期性边界条件
        N = Number+1
        cell0[0][0] = []
        cell0[0][K+1] = []
        cell0[K+1][0] = []
        cell0[K+1][K+1] = []
        for i in range(1,K+1):
            cell0[0][i] = []
            cell0[K+1][i] = []
            cell0[i][K+1] = []
            cell0[i][0] = []
        for j in cell0[K][K]:
            position1[N][0] = position1[j][0]-length
            position1[N][1] = position1[j][1]-length
            cell0[0][0].append(N)
            R[N] = R[j]
            N = N+1
        for i in range(1,K+1):
            for j in cell0[i][K]:
                position1[N][0] = position1[j][0]
                position1[N][1] = position1[j][1]-length
                cell0[i][0].append(N)
                R[N] = R[j]
                N = N+1
        for j in cell0[1][K]:
            position1[N][0] = position1[j][0]+length
            position1[N][1] = position1[j][1]-length
            cell0[K+1][0].append(N)
            R[N] = R[j]
            N = N+1
        for i in range(1,K+1):
            for j in cell0[1][i]:
                position1[N][0] = position1[j][0]+length
                position1[N][1] = position1[j][1]
                cell0[K+1][i].append(N)
                R[N] = R[j]
                N = N+1
        for j in cell0[1][1]:
            position1[N][0] = position1[j][0]+length
            position1[N][1] = position1[j][1]+length
            cell0[K+1][K+1].append(N)
            R[N] = R[j]
            N = N+1
        for i in range(K,0,-1):
            for j in cell0[i][1]:
                position1[N][0] = position1[j][0]
                position1[N][1] = position1[j][1]+length
                cell0[i][K+1].append(N)
                R[N] = R[j]
                N = N+1
        for j in cell0[K][1]:
            position1[N][0] = position1[j][0]-length
            position1[N][1] = position1[j][1]+length
            cell0[0][K+1].append(N)
            R[N] = R[j]
            N = N+1
        for i in range(K,0,-1):
            for j in cell0[K][i]:
                position1[N][0] = position1[j][0]-length
                position1[N][1] = position1[j][1]
                cell0[0][i].append(N)
                R[N] = R[j]
                N = N+1
        #print(cell0)
        
        #判断粒子的运动是否会发生碰撞
        for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]+1]+cell0[cellroom[0]-1][cellroom[1]-1]+cell0[cellroom[0]][cellroom[1]+1] \
            +cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]+1][cellroom[1]+1]+cell0[cellroom[0]+1][cellroom[1]-1]:
            if (chosen != j) & ((position1[chosen][0]-position1[j][0])**2+(position1[chosen][1]-position1[j][1])**2-(R[chosen]+R[j])**2<0):
                cell0[int(position1[chosen][0]//cellsize+1)][int(position1[chosen][1]//cellsize+1)].remove(chosen)
                position1[chosen][0] = originx1
                position1[chosen][1] = originy1
                position2[chosen][0] = originx2
                position2[chosen][1] = originy2
                cellist1(position1,chosen)
                cell0[int(originx1//cellsize+1)][int(originy1//cellsize+1)].append(chosen)
                
    for i in range(Number):
        MSD[t]=MSD[t]+(position1[i][0]-position0[i][0])**2+(position1[i][1]-position0[i][1])**2/Number
    print(MSD[t])

#绘制粒子MSD图像

for i in range(stime):
    ltime[i] = math.log(time[i])
    lMSD[i] = math.log(MSD[i])
plt.plot(ltime,lMSD)
plt.show()
