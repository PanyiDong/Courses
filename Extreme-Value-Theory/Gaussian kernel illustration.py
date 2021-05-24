import os
import sys
import pandas as pd
from openpyxl import load_workbook
import time
import random
import math
import seaborn
import numpy as np
import matplotlib
import seaborn.palettes
import seaborn.utils
#%matplotlib notebook
import matplotlib.pyplot as plt
import scipy.stats
from scipy import ndimage
from pandas.plotting import autocorrelation_plot
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.offsetbox as offsetbox
from matplotlib.ticker import StrMethodFormatter
import matplotlib.image as mpimg

dx = 0.01
length = int(6 / dx) + 1
x = [0 for i in range(length)]
y1 = [0 for i in range(length)]
y2 = [0 for i in range(length)]
y3 = [0 for i in range(length)]
y4 = [0 for i in range(length)]
y5 = [0 for i in range(length)]
y = [0 for i in range(length)]
mu1 = -2
mu2 = -1
mu3 = 0
mu4 = 1
mu5 = 2
sigma1 = 0.7
sigma2 = 0.7
sigma3 = 0.7
sigma4 = 0.7
sigma5 = 0.7

for i in range(length) :
    x[i] = (i - int(3 / dx)) * dx
    y1[i] = 0.7 * math.exp(-(x[i] - mu1) ** 2 / (2 * sigma1 ** 2)) / math.sqrt(2 * math.pi * sigma1 ** 2)
    y2[i] = 1.2 * math.exp(-(x[i] - mu2) ** 2 / (2 * sigma2 ** 2)) / math.sqrt(2 * math.pi * sigma2 ** 2)
    y3[i] = 1.5 * math.exp(-(x[i] - mu3) ** 2 / (2 * sigma3 ** 2)) / math.sqrt(2 * math.pi * sigma3 ** 2)
    y4[i] = 1.2 * math.exp(-(x[i] - mu4) ** 2 / (2 * sigma4 ** 2)) / math.sqrt(2 * math.pi * sigma4 ** 2)
    y5[i] = 0.7 * math.exp(-(x[i] - mu5) ** 2 / (2 * sigma5 ** 2)) / math.sqrt(2 * math.pi * sigma5 ** 2)
    y[i] = y1[i] + y2[i] + y3[i] + y4[i] + y5[i]

plt.figure()
plt.plot(x, y1, 'r--')
plt.plot(x, y2, 'r--')
plt.plot(x, y3, 'r--')
plt.plot(x, y4, 'r--')
plt.plot(x, y5, 'r--')
plt.plot(x, y, 'b')
plt.gca().get_xaxis().set_visible(False)
plt.gca().get_yaxis().set_visible(False)
plt.savefig('Gaussian kernel illustration.PNG', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
plt.show()
plt.close()