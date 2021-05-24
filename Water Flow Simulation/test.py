import sympy
import math
from scipy import integrate
import numpy as np

xi = sympy.Symbol('xi')
g = 9.81
#func = lambda xi: xi * np.sqrt(2 * 9.8 * h - (xi - mu) ** 2)

def test() :
    return 1

print(test())

def func(indicator, mu, h) :
    if (indicator == 0) :
        return lambda xi: xi * np.sqrt(2 * 9.8 * h - (xi - mu) ** 2) * max(0, xi)
    elif (indicator == 1) :
        return lambda xi: (xi ** 2) * np.sqrt(2 * 9.8 * h - (xi - mu) ** 2) * max(0, xi)

def func1() :
    return lambda xi: max(1, xi)

def Min(indicator, h, mu, deltaW, order) :
    if (indicator == 0) :
        return lambda xi: (xi ** order) * np.sqrt(max(0, 2 * g * h - (xi - mu) ** 2)) / (math.pi * g)

y1 = integrate.quad(Min(0, 0.05, 0, 0, 1), 0, +float('inf'))[0]
    
y = integrate.quad(func1(), -2, 2)[0]

print(y)
