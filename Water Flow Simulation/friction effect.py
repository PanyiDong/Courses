# For this part, we check three domains of friction factor alpha with alpha < 1, alpha = 1, alpha > 1
# And the model employs constant rainfall-runoff process with St. Vernant equations

# Topography Z = 0.1
# Infiltration rate I = 0, recharge rate R = 1
# At time 0, h = q = 1 (q = h * mu, mu for flow speed, h for water height, q for momentum of flow)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from matplotlib import rcParams

matplotlib.matplotlib_fname()

interval = 0.01
T = 1
timelen = int(T / interval) + 1

Z0 = 0.1
Z = [[Z0 for i in range(timelen)] for j in range(3)]
h = [[0 for i in range(timelen)] for j in range(3)]
H = [[0 for i in range(timelen)] for j in range(3)]
mu = [[0 for i in range(timelen)] for j in range(3)]
q = [[0 for i in range(timelen)] for j in range(3)]
t = [0 for i in range(timelen)]

for i in range(timelen) :
    t[i] = i * interval

I = 0
R = 1
S = R - I

for i in range(3) :
    h[i][0] = 1
    H[i][0] = h[i][0] + Z[i][0]
    q[i][0] = 1
    mu[i][0] = q[i][0] / h[i][0]

for n in range(3) :
    if (n == 0) :
        alpha = 0.5
    elif (n == 1) :
        alpha = 1
    elif (n == 2) :
        alpha = 1.5

    for i in range(timelen - 1) :
        h[n][i + 1] = h[n][i] + interval
        q[n][i + 1] = q[n][i] + (1 - alpha) * q[n][i] * interval / h[n][i]
        H[n][i + 1] = h[n][i + 1] + Z[n][i + 1]
        mu[n][i + 1] = q[n][i + 1] / h[n][i + 1]

plt.subplots()
plt.plot(t, q[0][:], linewidth = 2, color = 'red', label = r'$\alpha =0.5$')
plt.plot(t, q[1][:], linewidth = 2, color = 'blue', label = r'$\alpha =1.0$')
plt.plot(t, q[2][:], linewidth = 2, color = 'black', label = r'$\alpha =1.5$')
plt.legend()
plt.xlabel('t')
plt.ylabel('q(t,x)')
plt.title('momentum')
plt.savefig('momentum_plot.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches = 0)
plt.show()
plt.close()

plt.subplots()
plt.plot(t, mu[0][:], linewidth = 2, color = 'red', label = r'$\alpha =0.5$')
plt.plot(t, mu[1][:], linewidth = 2, color = 'blue', label = r'$\alpha =1.0$')
plt.plot(t, mu[2][:], linewidth = 2, color = 'black', label = r'$\alpha =1.5$')
plt.legend()
plt.xlabel('t')
plt.ylabel(r'$\mu(t,x)$')
plt.title('velocity')
plt.savefig('velocity_plot.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches = 0)
plt.show()
plt.close()

fig, ax = plt.subplots()
fig.set_tight_layout(True)
ax.axis([0, 10.3, 0, 2.2])

ax.axhline(y = Z0, xmin = 0, xmax = 10/10.34, linewidth = 3, color = 'brown')
ax.axhspan(ymin = 0, ymax = Z0, xmin = 0, xmax = 10/10.3, facecolor = 'brown', alpha = 0.5)

def update(i) :
    #label = 'timestep: '+str(round(i * interval,4))
    #ax.set_xlabel(label)
    #print(label)
    linem1.set_ydata(H[0][i + 1])
    linem2 = ax.axhspan(ymin = Z0, ymax = H[0][i + 1], xmin = 0, xmax = 10/10.3, facecolor = 'blue', alpha = 0.3)
    return linem1, linem2, ax

linem1 = ax.axhline(y = H[0][0], xmin = 0, xmax = 10/10.34, linewidth = 3, color = 'blue')
linem2 = ax.axhspan(ymin = Z0, ymax = H[0][0], xmin = 0, xmax = 10/10.3, facecolor = 'blue', alpha = 0)
ani = FuncAnimation(fig, update, frames = np.arange(0, timelen - 1), interval = 0.5, blit = False)
#writergif = animation.PillowWriter(fps=30) 
#matplotlib.rcParams['animation.convert_path'] = 'D:/Program Files/ImageMagick-7.0.10-Q16/magick.exe'
ani.save('surface.gif', writer = 'imagemagick', fps = 30)
#plt.show()
#plt.close()
