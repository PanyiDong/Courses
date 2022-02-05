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

totalp = 0
p_left = 1700 / 5978
p_right = 1733 / 5978
p_still = 1 - p_left - p_right

for i in range(10000) :
    print(i,C2(i + 1,i + 33,0.5))
    totalp = totalp + C2(i + 1,i + 33,0.5)

print('average',totalp)