#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#规定常数,position0为初始粒子分布，position1为区域边界下的位置，posiion2为全局位置
sigma=0.1
meanR=1
Number=4756
length=200
K=5
cellsize=length/K
dlumda=0.02
position0 = [([0] * 2) for i in range(Number)]
position1 = [([0] * 2) for i in range(Number)]
position2 = [([0] * 2) for i in range(Number)]
R=[(0 * 1) for i in range(Number)]

#定义空白cell list区域并写出规划粒子的函数
cell0 = []
rows = K
columns = K
for row in range(rows):
    cell0.append([])
    for column in range(columns):
        cell0[row].append([])

def cellist(position0,i):
    cell0[int(position0[i][0]//cellsize)][int(position0[i][1]//cellsize)].append(i)
    return [int(position0[i][0]//cellsize),int(position0[i][1]//cellsize)]

#生成满足正态分布的粒子半径并去除不需要的部分
i=0
random.seed(Number)
while i<Number:
    R[i] = random.gauss(meanR, sigma)
    if abs(R[i]-1)-3*sigma>0:
        i=i-1
    i=i+1

#算出粒子的体积分数
V=0
j=0
for j in range(Number):
    V=V+math.pi*R[j]**2
Phi=V/length**2
print('粒子的体积分数为%.2f' % Phi)

#随机生成粒子位置并列入list中
i=0
position0[0][0]=random.uniform(0,length)
position0[0][1]=random.uniform(0,length)
cellist(position0,i)
i=1
while i<Number:
    cellroom=[0,0]
    position0[i][0]=random.uniform(0,length)
    position0[i][1]=random.uniform(0,length)
    cellroom=cellist(position0,i)
    if cellroom[0]==0:
        if cellroom[1]==0:
            for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]][cellroom[1]+1]+cell0[cellroom[0]+1][cellroom[1]+1]:
                if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
        elif cellroom[1]==4:
            for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]-1]:
                if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
        else:
            for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]][cellroom[1]+1]+cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]-1]+cell0[cellroom[0]+1][cellroom[1]+1]:
                if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
    elif cellroom[0]==4:
        if cellroom[1]==0:
            for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]][cellroom[1]+1]+cell0[cellroom[0]-1][cellroom[1]+1]:
                if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
        elif cellroom[1]==4:
            for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]-1][cellroom[1]-1]:
                if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
        else:
            for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]][cellroom[1]+1]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]-1]+cell0[cellroom[0]-1][cellroom[1]+1]:
                if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
    elif cellroom[1]==0:
        for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]][cellroom[1]+1]+cell0[cellroom[0]+1][cellroom[1]+1]+cell0[cellroom[0]-1][cellroom[1]+1]:
            if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
    elif cellroom[1]==4:
        for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]-1][cellroom[1]-1]+cell0[cellroom[0]+1][cellroom[1]-1]:
            if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
    else:
        for j in cell0[cellroom[0]][cellroom[1]]+cell0[cellroom[0]][cellroom[1]+1]+cell0[cellroom[0]][cellroom[1]-1]+cell0[cellroom[0]-1][cellroom[1]]+cell0[cellroom[0]-1][cellroom[1]-1]+cell0[cellroom[0]-1][cellroom[1]+1] \
        +cell0[cellroom[0]+1][cellroom[1]]+cell0[cellroom[0]+1][cellroom[1]-1]+cell0[cellroom[0]+1][cellroom[1]+1]:
            if (position0[i][0]-position0[j][0])**2+(position0[i][1]-position0[j][1])**2-(R[i]+R[j])**2<0:
                    continue
    i=i+1
print(position0)

#将初始粒子分布分配到position1,position2
for i in range(Number):
    postion1[i][0]=position0[i][0]
    postion1[i][1]=position0[i][1]
    postion2[i][0]=position0[i][0]
    postion2[i][1]=position0[i][1]

#模拟粒子运动
for t in range(1000):
    MSD(t)=0
    time(t)=t
    for ts in range(100):
        chosen=random.randint(0,Number-1)
        movement[0]=random.uniform(-dlumda,dlumda)
        movement[1]=random.uniform(-dlumda,dlumda)
        position1[chosen][0]=position1[chosen][0]+movement[0]
        position1[chosen][1]=position1[chosen][1]+movement[1]
        cellroom=cellist(position1,chosen)
        #判断粒子的运动是否会发生碰撞
    for i in range(Number):
        MSD(time)=MSD(time)+(position1[i][0]-position0[i][0])**2+(position1[i][1]-position0[i][1])**2

#绘制粒子MSD图像
plt.plot(time,MSD)
plt.show()
    
