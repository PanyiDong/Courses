# Water flow simulation of St. Venant system with kinetic numerical method
# The topography of bed: linear slope
# Water interaction: only precipitation, no infiltration

import math
import matplotlib.pyplot as plt
import sympy
from scipy import integrate
import numpy as np

# Define constants
g = 9.81 # Gravitational acceleration
L = 4 # Domain length
N = 1000 # Meshpoints
deltax = L / N # Interval length on x-axis
CFL = 0.95
alpha = 1 # Friction factor
T = 50 # Total time simulated
t = 0 # Initial time
trecord = []
trecord.append(t)
I = 0 # Infiltration
xi = sympy.Symbol('xi')

# Define initial conformation
# Topography of bed
Z = [(0.2 - i * deltax / 20) for i in range(N + 1)]
x = [(i * deltax) for i in range(N + 1)]
xhalf = [((i - 0.5) * deltax) for i in range(N + 2)] # Cells

# Intial water flow
h0 = 0
q0 = 0
if (h0 == 0) :
    mu0 = 0
else :
    mu0 = 0
h = []
h.append([h0 for i in range(N + 1)])
q = []
q.append([q0 for i in range(N + 1)])
mu = []
mu.append([mu0 for i in range(N + 1)])

# Define calculation functions

# Precipitation/Recharge R
def R(t, x) :
    if (t >= 5 and t<= 25 and x >= 0 and x <= 3.95) :
        return 50
    else :
        return 0

# Water interaction S
def S(t, x) :
    return R(t, x) - I

# Calculate CFL time steps
def CFLtime(h, mu, CFL, deltax) :
    
    lenmu = len(mu)
    comp = [0 for i in range(lenmu)]
    for i in range(lenmu) :
        if (h[i] < 0) :
            print('Negative h error!')
        else :
            comp[i] = abs(mu[i]) + np.sqrt(2 * g * h[i])
    
    deno = max(comp)
    if (deno == 0) :
        CFLtime = 0.01
    else :
        #CFLtime = CFL * deltax / deno
        CFLtime = 0.001
    
    return CFLtime

# W energy function
def Win(Z, h, mu, x, t) :
    W = [0 for i in range(N + 3)]
    for i in range(N + 3) :
        if (i == 0) :
            W[i] = Z[i]
        elif (i == N + 2) :
            W[i] = 0
        else :
            W[i] = Z[i - 1]
            for j in range(i) :
                if (h[j] != 0) :
                    W[i] = W[i] + alpha * R(x[i - 1], t) * mu[j] / (g * h[j])

    return W

# W energy barrier
def deltaWin(indicator, W) :
    deltaW = [0 for i in range(N + 1)]
    if (indicator == '+') :
        for i in range(N + 1) :
            deltaW[i] = W[i + 2] - W[i + 1]
        return deltaW
    elif (indicator == '-') :
        for i in range(N + 1) :
            deltaW[i] = W[i] - W[i + 1]
        return deltaW

# Barrenblatt kinetic weighting function
def chi(omega) :
    return lambda xi: np.sqrt(max(0, 2 * g - omega ** 2)) / (math.pi * g)

# Semi-discretized kinetic energy
def Min(indicator, h, mu, deltaW, order) :
    if (indicator == 0) :
        return lambda xi: (xi ** order) * np.sqrt(max(0, 2 * g * h - (xi - mu) ** 2)) / (math.pi * g)
    if (indicator == 1) :
        return lambda xi: (xi ** order) * np.sqrt(max(0, 2 * g * h - (-xi - mu) ** 2)) / (math.pi * g)
    if (indicator == 2) :
        return lambda xi: (xi ** order) * np.sqrt(max(0, 2 * g * h - (-np.sqrt(max(0, xi ** 2 - 2 * g * deltaW)) - mu) ** 2)) / (math.pi * g)
    if (indicator == 3) :
        return lambda xi: (xi ** order) * np.sqrt(max(0, 2 * g * h - (np.sqrt(max(0, xi ** 2 - 2 * g * deltaW)) - mu) ** 2)) / (math.pi * g)

# Fhalf function calculation
#def Fhalf(state, h, mu, deltaW, n) :
    #if (state == 'plus' and n == 0) :
        #y1 = integrate.quad(Min(0, h, mu, 1), max(0, mu - np.sqrt(2 * g * h)), mu + np.sqrt(2 * g * h))[0]
        #y2 = integrate.quad(Min(1, h, mu, 1), max(-np.sqrt(2 * g * deltaW), mu - np.sqrt(2 * g * h)), min(0, -mu + np.sqrt(2 * g * h)))[0]
        #y3 = integrate.quad(Min(2, h, mu, 1), -np.sqrt(2 * g * deltaW + (mu - 2 * g * h) ** 2), -np.sqrt(2 * g * deltaW))[0]
        #return y1 + y2 + y3
    #elif (state == 'plus' and n == 1) :
        #y1 = integrate.quad(Min(0, h, mu, 2), max(0, mu - np.sqrt(2 * g * h)), mu + np.sqrt(2 * g * h))[0]
        #y2 = integrate.quad(Min(1, h, mu, 2), max(-np.sqrt(2 * g * deltaW), mu - np.sqrt(2 * g * h)), min(0, -mu + np.sqrt(2 * g * h)))[0]
        #y3 = integrate.quad(Min(2, h, mu, 2), -np.sqrt(2 * g * deltaW + (mu - 2 * g * h) ** 2), -np.sqrt(2 * g * deltaW))[0]
        #return y1 + y2 + y3
    #elif (state == 'minus' and n == 0) :
        #y1 = integrate.quad(Min(0, h, mu, 1), min(0, mu - np.sqrt(2 * g * h)), 0)[0]
        #y2 = integrate.quad(Min(1, h, mu, 1), 0, min(np.sqrt(2 * g * deltaW), 0, np.sqrt(2 * g * h) - mu))[0]
        #y3 = integrate.quad(Min(3, h, mu, 1), np.sqrt(2 * g * deltaW), np.sqrt(2 * g * deltaW + (mu + 2 * g * h) ** 2))[0]
        #return y1 + y2 + y3
    #elif (state == 'minus' and n == 1) :
        #y1 = integrate.quad(Min(0, h, mu, 2), min(0, mu - np.sqrt(2 * g * h)), 0)[0]
        #y2 = integrate.quad(Min(1, h, mu, 2), 0, min(np.sqrt(2 * g * deltaW), 0, np.sqrt(2 * g * h) - mu))[0]
        #y3 = integrate.quad(Min(3, h, mu, 2), np.sqrt(2 * g * deltaW), np.sqrt(2 * g * deltaW + (mu + 2 * g * h) ** 2))[0]
        #return y1 + y2 + y3

def Fhalf(state, h, h2, mu, mu2, deltaW, deltaW2, n) :
    if (state == 'plus') :
        y1 = integrate.quad(Min(0, h, mu, deltaW, n + 1), 0, +float('inf'))[0]
        y2 = integrate.quad(Min(1, h, mu, deltaW, n + 1), -np.sqrt(max(0, 2 * g * deltaW)), 0)[0]
        y3 = integrate.quad(Min(2, h2, mu2, deltaW, n + 1), -float('inf'), -np.sqrt(max(0, 2 * g * deltaW)))[0]
        return y1 + y2 + y3
    elif (state == 'minus') :
        y1 = integrate.quad(Min(0, h, mu, deltaW, n + 1), -float('inf'), 0)[0]
        y2 = integrate.quad(Min(1, h, mu, deltaW, n + 1), 0, np.sqrt(max(0, 2 * g * deltaW)))[0]
        y3 = integrate.quad(Min(3, h2, mu2, deltaW2, n + 1), np.sqrt(max(0, 2 * g * deltaW2)), +float('inf'))[0]
        return y1 + y2 + y3

open('TailMomentum.txt','w')

TailM = open('TailMomentum.txt','w')

TailM.seek(0)
TailM.truncate()

print('%-16s' % 'Time', '%-16s' % 'TailVelocity', '%-16s' % 'TailHeight', '%-16s' % 'TailMomentum', file = TailM)
print('%-16f' % t, '%-16f' % mu[0][N], '%-16f' % h[0][N], '%-16f' % q[0][N], file = TailM)

# Water flow simulation of St. Vernant system
count = 0
tcount = 0
while (t <= T) :

    deltat = CFLtime(h[count][:], mu[count][:], CFL, deltax)

    # Define W energy barrier
    W = [0 for i in range(N + 3)]
    deltaW = [[0 for i in range(N + 1)] for j in range(2)]

    W[:] = Win(Z, h[count][:], mu[count][:], x, t)
    deltaW[0][:] = deltaWin('+', W)
    deltaW[1][:] = deltaWin('-', W)

    hnew = [0 for i in range(N + 1)]
    qnew = [0 for i in range(N + 1)]
    munew = [0 for i in range(N + 1)]

    for i in range(N + 1) :
        
        #print(deltat * (Fhalf('plus', mu[count][i], h[count][i], deltaW[0][i], 0) - Fhalf('minus', mu[count][i], h[count][i], deltaW[0][i], 0)) / deltax, deltat * (Fhalf('plus', mu[count][i], h[count][i], deltaW[1][i], 1) - Fhalf('minus', mu[count][i], h[count][i], deltaW[1][i], 1)) / deltax)
        Fhalfplus0 = Fhalf('plus', h[count][i], h[count][min(N, i + 1)], mu[count][i], mu[count][min(N, i + 1)], deltaW[0][i], deltaW[1][i], 0)
        Fhalfplus1 = Fhalf('plus', h[count][i], h[count][max(0, i - 1)], mu[count][i], mu[count][max(0, i - 1)], deltaW[0][i], deltaW[1][i], 1)
        Fhalfminus0 = Fhalf('minus', h[count][i], h[count][min(N, i + 1)], mu[count][i], mu[count][min(N, i + 1)], deltaW[0][i], deltaW[1][i], 0)
        Fhalfminus1 = Fhalf('minus', h[count][i], h[count][max(0, i - 1)], mu[count][i], mu[count][max(0, i - 1)], deltaW[0][i], deltaW[1][i], 1)
        
        hnew[i] = h[count][i] - deltat * (Fhalfplus0 - Fhalfminus0) / deltax + deltat * S(t, x[i])
        qnew[i] = q[count][i] - deltat * (Fhalfplus1 - Fhalfminus1) / deltax + deltat * S(t, x[i]) * mu[count][i]

        if (hnew[i] == 0) :
            munew[i] = 0
        else :
            munew[i] = qnew[i] / hnew[i]

    h.append(hnew)
    q.append(qnew)
    mu.append(munew)

    count = count + 1
    t = t + deltat
    trecord.append(t)

    print('%-16f' % t, '%-16f' % munew[N], '%-16f' % hnew[N], '%-16f' % qnew[N], file = TailM)

    if (t >= 10 * (tcount + 1)) :
        print('t is:', t)
        tcount = tcount + 1

TailM.close()
tailmomentum = [q[i][N] for i in range(count + 1)]

plt.subplot()
#plt.axis([-0.2, 250.2])
plt.plot(trecord, tailmomentum, color = 'red', label = 'momentum of water flow')
plt.legend()
plt.savefig('Momentum.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches = 0)
plt.show()
plt.close()