import os
import sys
import pandas as pd
import geopandas as gpd
import contextily as ctx
from pyproj import Proj, transform
import netCDF4
from openpyxl import load_workbook
import time
import random
import numpy
import matplotlib
#%matplotlib notebook
import matplotlib.pyplot as plt
import scipy.stats
from pandas.plotting import autocorrelation_plot
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.offsetbox as offsetbox
from matplotlib.ticker import StrMethodFormatter

def cal(x) :
    x = 2
    return x

x = 0

cal(x)

print(x)