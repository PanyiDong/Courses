import numpy as np 
import math
import matplotlib.pyplot as plt
import random

def Rangauss() :
    #W = 2
    #while W > 1 or W < -1 :
        #W = random.gauss(0,1)
    W = random.uniform(-1, 1)
    return W

#Define constants

L = 1
A = 20
lambdaE = 0.1
rho = 0.11  # g/cm3
eta = 0.11  # pa*s
n0kT = 8.8
deltat = 0.001 # s
K0 = 2500

#Calculate constants defined by original constants

deltay = L / A
deltat_ = deltat / lambdaE # s

ya = np.zeros(20)
for i in range(20) :
    ya[i] = ( i + 1 ) * deltay

a1 = eta * deltat / ( rho * (deltay ** 2) )
a2 = deltat / ( rho * deltay ) 

#Construct velocity feild equation

VectorM = np.zeros((20,20))
for i in range(20) :
    VectorM[i,i] = 1 + 2 * a1
    if i == 0 :
        VectorM[0,1] = - a1
    elif i == 19 :
        VectorM[19,18] = - a1
    else :
        VectorM[i,i-1] = - a1
        VectorM[i,i+1] = - a1

#Calculate velocity field and stress field as time passes

for a in range(1) :

    if a == 0 :
        b = 100
    elif a == 1 :
        b = 20
    elif a == 2 :
        b = 100
    else :
        b = 400
    
    #Set initial value

    v = np.zeros((20,b + 1))
    U = np.zeros((20,b + 1))
    v_output = np.zeros(20)
    tau = np.zeros((20,b + 1))
    tau_output = np.zeros(20)
    M = np.zeros((((5,20,b + 1,2500))))
    N = np.zeros(((5,b + 1,2500)))

    v[0,0] = 1

    for n in range(5) :
        for i in range(20) :
            for K in range(2500) :
                M0 = Rangauss()
                N0 = Rangauss()
                M[n,i,0,K] = M0 / math.sqrt(M0 ** 2 + N0 ** 2)
                N[n,0,K] = N0 / math.sqrt(M0 ** 2 + N0 ** 2)

    for i in range(20) :
        for n in range(5) :
            for k in range(2500) :
                tau[i,0] = tau[i,0] + n0kT * M[n,i,0,k] * N[n,0,k] / K0

    for i in range(20) :
        if i < 19 :
            U[i,0] = a2 * ( tau[i + 1,0] - tau[i,0] ) + v[i,0]
        else :
            U[i,0] = - a2 * tau[i,0] + v[i,0]

    for j in range(b) :

        v_Cal = np.array(range(20)).reshape(20,1)
        U_Cal = np.array(range(20)).reshape(20,1)
        v_Sol = np.array(range(20)).reshape(20,1)
        U_Sol = np.array(range(20)).reshape(20,1)
        for i in range(20) :
            v_Cal[i] = 0
            U_Cal[i] = 0
            v_Sol[i] = 0
            U_Sol[i] = 0
        
        for i in range(20) :
            v_Cal[i] = v[i,j]
            U_Cal[i] = U[i,j]
            
        #Calculate velocity field

        v_Sol = np.linalg.solve(VectorM,U_Cal)
        v_Sol = sorted(v_Sol,reverse = True)

        #Determine horizontal vector field M

        for n in range(5) :
            for i in range(20) :
                for k in range(2500) :
                    if n == 0 :
                        if i == 0 :
                            M[n,i,j + 1,k] = v[i,j] * N[n,j,k] * deltat_ / deltay + M[n + 1,i,j,k] * deltat_ / 4 + (1 - deltat_ / 2) * M[n + 1,i,j,k] + math.sqrt(deltat_ / 2) * (Rangauss() - Rangauss())
                        else :
                            M[n,i,j + 1,k] = (v[i,j]-v[i-1,j]) * N[n,j,k] * deltat_ / deltay + M[n + 1,i,j,k] * deltat_ / 4 + (1 - deltat_ / 2) * M[n + 1,i,j,k] + + math.sqrt(deltat_ / 2) * (Rangauss() - Rangauss())
                    elif n == 4 :
                        if i == 0 :
                            M[n,i,j + 1,k] = v[i,j] * N[n,j,k] * deltat_ / deltay + M[n - 1,i,j,k] * deltat_ / 4 - math.sqrt(deltat_ / 2) * Rangauss()
                        else :
                            M[n,i,j + 1,k] = (v[i,j]-v[i-1,j]) * N[n,j,k] * deltat_ / deltay + M[n - 1,i,j,k] * deltat_ / 4 - math.sqrt(deltat_ / 2) * Rangauss()
                    else :
                        if i == 0 :
                            M[n,i,j + 1,k] = v[i,j] * N[n,j,k] * deltat_ / deltay + (M[n + 1,i,j,k] + M[n - 1,i,j,k]) * deltat_ / 4 + (1 - deltat_ / 2) * M[n + 1,i,j,k] + math.sqrt(deltat_ / 2) * (Rangauss() - Rangauss())
                        else :
                            M[n,i,j + 1,k] = (v[i,j]-v[i-1,j]) * N[n,j,k] * deltat_ / deltay + (M[n + 1,i,j,k] + M[n - 1,i,j,k]) * deltat_ / 4 + (1 - deltat_ / 2) * M[n + 1,i,j,k] + math.sqrt(deltat_ / 2) * (Rangauss() - Rangauss())
    
        #Determine vertical vector field N

        for n in range(5) :
            for k in range(2500) :
                if n == 0 :
                    N[n,j + 1,k] = N[n + 1,j,k] * deltat_ / 4 + (1 - deltat_ / 2) * N[n,j,k] + math.sqrt(deltat_ / 2) * (Rangauss() - Rangauss())
                elif n == 4 :
                    N[n,j + 1,k] = N[n - 1,j,k] * deltat_ / 4 + (1 - deltat_ / 2) * N[n,j,k] - math.sqrt(deltat_ / 2) * Rangauss()
                else :
                    N[n,j + 1,k] = (N[n + 1,j,k] + N[n - 1,j,k]) * deltat_ / 4 + (1 - deltat_ / 2) * N[n,j,k] + math.sqrt(deltat_ / 2) * (Rangauss() - Rangauss())

        #Determin stress field

        for i in range(20) :
            for n in range(5) :
                for K in range(2500) :
                    tau[i,j + 1] = tau[i,j + 1] + n0kT * M[n,i,j + 1,k] * N[n,j + 1,k] / K0

        #Return velocity field and stress field 

        for i in range(20) :
            v[i,j + 1] = v_Sol[i]
              
        for i in range(20) :
            if i < 19 :
                U_Sol[i] =  a2 * ( tau[i + 1,j + 1] - tau[i,j + 1] ) + v[i,j + 1]
                U[i,j + 1] = U_Sol[i]
            else :
                U_Sol[i] =  - a2 * tau[i,j + 1] + v[i,j + 1]
                U[i,j + 1] = U_Sol[i]

        print(v_Sol) 

    for i in range(20) :
        v_output[i] = v[i,b]
        #tau_output[i] = tau[i,b]

    plt.plot(ya,v_output)
    #plt.plot(ya,tau_output)

#plt.xlim(0,1)
#plt.ylim(-0.2,1.0)
plt.show()           