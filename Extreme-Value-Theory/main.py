import os
import sys
import pandas as pd
import geopandas
import contextily as ctx
from pyproj import Proj, transform
import netCDF4
from netCDF4 import Dataset
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

#############################################################################################################################################################################################################
# Data Prcocessing 

# two sets of coordinates EPSG4326 with longitudes/latitudes and EPSG3857 for the mapping
P3857 = Proj(init='epsg:3857')
P4326 = Proj(init='epsg:4326')
P32630 = Proj(init='epsg:32630') # UTM 30 degree N coordinates

# Read in Station Coordinates
workbook = load_workbook('station coordinates(EPSG4326)_230.xlsx')
booksheet = workbook.get_sheet_by_name('Sheet1')

StationName = [item.value for item in list(booksheet.columns)[0]]
StationLat = [float(round(item.value,1)) for item in list(booksheet.columns)[1]]
StationLon = [float(round(item.value,1)) for item in list(booksheet.columns)[2]]

NoStation = len(StationName)

# Check if there are stations overlapped
overlap = 0
for i in range(len(StationName)) :
    for j in range(len(StationName) - i - 1) :
        if (StationLat[i] == StationLat[i + j + 1] and StationLon[i] == StationLon[i + j + 1]) :
            overlap = overlap + 1
            print('Overlapped stations are',i + 1, i + j + 2)

if (overlap > 0) :
    print('There are stations overlapped.')
    sys.exit(0)

# print(StationName)
# print(StationLat)
# print(StationLon)
# Read in precipitation data

nc = Dataset('Spain02_v5.0_DD_010reg_aa3d_pr.nc') # daily gridded precipitation and temperature datasets for Spain

DataLat = nc.variables['lat'][:] # observation lattitudes (degree north)
DataLon = nc.variables['lon'][:] # observation longtitudes (degree east)
DataPr = nc.variables['pr'][:] # observation precipitation by kg m-2, 3D data (two location parameters and time)
DataTime = nc.variables['time'][:] # observation time

DataPr = DataPr.filled(0)

for i in range(len(DataLat)) :
    DataLat[i] = round(DataLat[i], 1)
for i in range(len(DataLon)) :
    DataLon[i] = round(DataLon[i], 1)

# Check if any stations out of data boundary
for i in range(NoStation) :
    if (StationLat[i] < min(DataLat) or StationLat[i] > max(DataLat) or StationLon[i] < min(DataLon) or StationLon[i] > max(DataLon)) :
        print('Out of boundary station: ', i + 1)

# print(DataLat) # 79 latitudes in database
# print(DataLon.shape) # 138 longitudes in database
# print(DataPr.shape) # 24106 * 79 * 138 percipitation observations in database
#print(DataTime)

# 24106 days is exactly 66 years
DataYears = 66

def CoorTransform() :
    
    # Read in station and location statistics
    # Longitude is x and latitude is y on the map, and in this case, epsg4326 coordinates are read in
    df = pd.DataFrame(
        {'Station': StationName,
         'Latitude': StationLat,
         'Longitude': StationLon})

    # Construct location points
    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

    # Transfer EPSG4326 coordinates to EPSG3857 coordinates
    for i in range(NoStation):
        gdf.Longitude[i],gdf.Latitude[i] = transform(P4326, P3857, gdf.Longitude[i], gdf.Latitude[i])

    # Read in transformed data to reduce process time
    #with open ('Station_Coordinates.txt') as file_object :
        #lines01 = file_object.readlines()
    #dataset01 = [[] for i in range(len(lines01))]
    #dataset011 = [[] for i in range(len(lines01))]
    #for i in range(len(dataset01)):
        #dataset011[i][:] = (item for item in lines01[i].strip().split(' '))

    # Delete invalid data caused by space
    #for i in range(len(lines01)) :
        #for j in range(len(dataset011[i])) :
            #if dataset011[i][j] == '' :
                #continue
            #else :
                #dataset01[i].append(dataset011[i][j])

    #for i in range(NoStation) :
        #gdf.Latitude[i] = float(dataset01[i + 1][2])
        #gdf.Longitude[i] = float(dataset01[i + 1][3])
    
    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

    # Write station coordinates (two forms)
    #open('Station_Coordinates.txt','w')

    #stationcoor = open('Station_Coordinates.txt','w')

    #stationcoor.seek(0)
    #stationcoor.truncate()

    #print('%-16s' % 'StationEP4326Lat', '%-16s' % 'StationEP4326Lon', '%-16s' % 'StationEP3857Lat', '%-16s' % 'StationEP3857Lon', file = stationcoor)

    #for i in range(NoStation) :
        #print('%-16f' % StationLat[i], '%-16f' % StationLon[i], '%-16f' % gdf.Latitude[i], '%-16f' % gdf.Longitude[i], file = stationcoor)

    #stationcoor.close()


# Construct epsg4326 coordinates for data
EP4326DataLat = [0 for i in range(len(DataLat) * len(DataLon))]
EP4326DataLon = [0 for i in range(len(DataLat) * len(DataLon))]

count = 0
for i in range(len(DataLat)) :
    for j in range(len(DataLon)) :
        EP4326DataLat[count] = DataLat[i]
        EP4326DataLon[count] = DataLon[j]
        count = count + 1

# Write EPSG4326 coordinates for data
#open('Data_EP4326_Coordinates.txt','w')

#coor1 = open('Data_EP4326_Coordinates.txt','w')

#coor1.seek(0)
#coor1.truncate()

#for i in range(len(DataLat) * len(DataLon) + 1) :
    #if ( i == 0) :
        #print( '%-16s' % 'Lattitude', '%-16s' % 'Longitude', file = coor1)
    #else :
        #print('%-16s' % EP4326DataLat[i - 1], '%-16s' % EP4326DataLon[i - 1], file = coor1)
#coor1.close()

# Construct epsg3857 coordinates for data
EP3857DataLat = [0 for i in range(len(DataLat) * len(DataLon))]
EP3857DataLon = [0 for i in range(len(DataLat) * len(DataLon))]

#for i in range(len(DataLat) * len(DataLon)) :
    #EP3857DataLon[i],EP3857DataLat[i] = transform(P4326, P3857, EP4326DataLon[i], EP4326DataLat[i])

# Read in transformed coordinates data to reduce process time
with open ('Data_EP3857_Coordinates.txt') as file_object :
    lines02 = file_object.readlines()
dataset02 = [[] for i in range(len(lines02))]
dataset022 = [[] for i in range(len(lines02))]
for i in range(len(dataset02)):
    dataset022[i][:] = (item for item in lines02[i].strip().split(' '))
    
# Delete invalid data caused by space
for i in range(len(lines02)) :
    for j in range(len(dataset022[i])) :
        if dataset022[i][j] == '' :
            continue
        else :
            dataset02[i].append(dataset022[i][j])

for i in range(len(DataLat) * len(DataLon)) :
    EP3857DataLat[i] = float(dataset02[i + 1][0])
    EP3857DataLon[i] = float(dataset02[i + 1][1])

# Write EPSG3857 coordinates for data
#open('Data_EP3857_Coordinates.txt','w')

#coor2 = open('Data_EP3857_Coordinates.txt','w')

#coor2.seek(0)
#coor2.truncate()

#for i in range(len(DataLat) * len(DataLon) + 1) :
    #if ( i == 0) :
        #print('%-16s' % 'Lattitude', '%-16s' % 'Longitude', file = coor2)
    #else :
        #print('%-16s' % round(EP3857DataLat[i - 1],4), '%-16s' % round(EP3857DataLon[i - 1],4), file = coor2)
#coor2.close()

# Convert epsg32630 coordinates for data
EP32630DataLat = [0 for i in range(len(DataLat) * len(DataLon))]
EP32630DataLon = [0 for i in range(len(DataLat) * len(DataLon))]

#for i in range(len(DataLat) * len(DataLon)) :
    #EP32630DataLon[i],EP32630DataLat[i] = transform(P4326, P32630, EP4326DataLon[i], EP4326DataLat[i])

# Write epsg32630 coordinates
#open('Data_EP32630_Coordinates.txt','w')

#coor3 = open('Data_EP32630_Coordinates.txt','w')

#coor3.seek(0)
#coor3.truncate()

#for i in range(len(DataLat) * len(DataLon) + 1) :
    #if ( i == 0) :
        #print('%-16s' % 'Lattitude', '%-16s' % 'Longitude', file = coor3)
    #else :
        #print('%-16s' % round(EP32630DataLat[i - 1],4), '%-16s' % round(EP32630DataLon[i - 1],4), file = coor3)
#coor3.close()

# Mapping stations' coordinates with percipitation data coordinates
MapLat = [0 for i in range(NoStation)]
MapLon = [0 for i in range(NoStation)]

for i in range(NoStation) :
    for j in range(len(DataLat)) :
        if (abs(DataLat[j] - StationLat[i]) < 0.01) :
                MapLat[i] = j
        continue
    for j in range(len(DataLon)) :
        if ((DataLon[j] - StationLon[i]) < 0.01) :
            MapLon[i] = j
        continue

# Write mapping array
#open('Map_Station_Data.txt','w')

#mapcoor = open('Map_Station_Data.txt','w')

#mapcoor.seek(0)
#mapcoor.truncate()

#print('%-16s' % 'Latitude', '%-16s' % 'Longtitude', '%-16s' % 'NoDataLat', '%-16s' % 'NoDataLon', file = mapcoor)

#for i in range(NoStation) :
    #print('%-16s' % StationLat[i], '%-16s' % StationLon[i], '%-16s' % MapLat[i], '%-16s' % MapLon[i], file = mapcoor)

#mapcoor.close()

# print(MapLat)
# print(MapLon)

# Write precipitation data
#file = open('Precipitation_Data.txt','w')

#pr = open('Precipitation_Data.txt','w')

#pr.seek(0)
#pr.truncate()

#print('%-16s' % 'Precipitation', '%-16s' % 'Time', '%-16s' % 'Latitude', '%-16s' % 'Longitude', file = pr)

#for t in range(len(DataTime)) :
    #for i in range(len(DataLat)) :
        #for j in range(len(DataLon)) :
            #print('%-16s' % DataPr[t][i][j], '%-16s' % DataTime[t], '%-16s' % DataLat[i], '%-16s' % DataLon[j], file = pr)
#pr.close()

def AvgStation() :

    # Calculate average daily percipitation at-sites
    AvgDDStationPr = [0 for i in range(NoStation)]

    for i in range(len(DataTime)) :
        for j in range(NoStation) :
            AvgDDStationPr[j] = AvgDDStationPr[j] + DataPr[i][MapLat[j]][MapLon[j]]

    for i in range(NoStation) :
        AvgDDStationPr[i] = AvgDDStationPr[i] / len(DataTime)

    #print(AvgDDStationPr)

    # Write average daily percipitation at-sites
    open('Average_Daily_Precipitaion_Station.txt','w')

    AvgDDPrStation = open('Average_Daily_Precipitaion_Station.txt','w')

    AvgDDPrStation.seek(0)
    AvgDDPrStation.truncate()

    print('%-20s' % 'Avrage Precipitaiton', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = AvgDDPrStation)

    for i in range(NoStation) :
        print('%-20s' % AvgDDStationPr[i], '%-20s' % StationLat[i], '%-20s' % StationLon[i], file = AvgDDPrStation)

    AvgDDPrStation.close()

    # Calculate average annual percipitation at-sites
    AvgYYStationPr = [0 for i in range(NoStation)]
    for i in range(NoStation) :
        AvgYYStationPr[i] = AvgDDStationPr[i] * len(DataTime) / DataYears

    #print(AvgYYStationPr)

    # Write average annual percipitation at-sites
    open('Average_Annual_Precipitaion_Station.txt','w')

    AvgYYPrStation = open('Average_Annual_Precipitaion_Station.txt','w')

    AvgYYPrStation.seek(0)
    AvgYYPrStation.truncate()

    print('%-20s' % 'Avrage Precipitaiton', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = AvgYYPrStation)

    for i in range(NoStation) :
        print('%-20s' % AvgYYStationPr[i],4, '%-20s' % StationLat[i], '%-20s' % StationLon[i], file = AvgYYPrStation)

    AvgYYPrStation.close()

    return AvgDDStationPr, AvgYYStationPr

def AvgNation():

    # Calculate nation-wide average daily percipitation
    AvgDDNationPr = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            for t in range(len(DataTime)) :
                AvgDDNationPr[i][j] = AvgDDNationPr[i][j] + DataPr[t][i][j] / len(DataTime)

    #print(AvgDDNationPr)

    # Write average daily percipitation nation-wide
    open('Average_Daily_Precipitaion_Spain.txt','w')

    AvgDDPrSp = open('Average_Daily_Precipitaion_Spain.txt','w')

    AvgDDPrSp.seek(0)
    AvgDDPrSp.truncate()

    print('%-20s' % 'Avrage Precipitaiton', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = AvgDDPrSp)

    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            print('%-20s' % AvgDDNationPr[i][j], '%-20s' % DataLat[i], '%-20s' % DataLon[j], file = AvgDDPrSp)

    AvgDDPrSp.close()
    
    # Calculate nation-wide average annual percipitation
    AvgYYNationPr = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            AvgYYNationPr[i][j] = AvgDDNationPr[i][j] * len(DataTime) / DataYears

    #print(AvgYYNationPr)

    # Write average annual percipitation nation-wide
    open('Average_Annual_Precipitaion_Spain.txt','w')

    AvgYYPrSp = open('Average_Annual_Precipitaion_Spain.txt','w')

    AvgYYPrSp.seek(0)
    AvgYYPrSp.truncate()

    print('%-20s' % 'Avrage Precipitaiton', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = AvgYYPrSp)

    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            print('%-20s' % AvgYYNationPr[i][j], '%-20s' % DataLat[i], '%-20s' % DataLon[j], file = AvgYYPrSp)

    AvgYYPrSp.close()

    return AvgDDNationPr, AvgYYNationPr

def MaxStaion() :
    
    # Calculate average annual daily maxima at-sites
    AvgYDMaxStationPrRecord = [[0 for i in range(DataYears)] for j in range(NoStation)]
    AvgYDMaxStationPr = [0 for i in range(NoStation)]

    count = 0
    # The data year follows common, common, leap, common, common, common, leap, ...
    for i in range(DataYears) :
        if ((i - 2) % 4 == 0) :
            YearLength = 366
        else :
            YearLength = 365
        for j in range(YearLength) :
            for k in range(NoStation) :
                if (j == 0) :
                    AvgYDMaxStationPrRecord[k][i] = DataPr[count][MapLat[k]][MapLon[k]]
                else :
                    if (DataPr[count][MapLat[k]][MapLon[k]] > AvgYDMaxStationPrRecord[k][i]) :
                        AvgYDMaxStationPrRecord[k][i] = DataPr[count][MapLat[k]][MapLon[k]]
            count = count + 1

    for i in range(NoStation) :
        for j in range(DataYears) :
            AvgYDMaxStationPr[i] = AvgYDMaxStationPr[i] + AvgYDMaxStationPrRecord[i][j] / DataYears

    # Write average annual daily maxima at-sites
    open('Average_Annual_Daily_Maxima_Station.txt','w')

    AvgYDMaxStaPr = open('Average_Annual_Daily_Maxima_Station.txt','w')

    AvgYDMaxStaPr.seek(0)
    AvgYDMaxStaPr.truncate()

    print('%-22s' % 'Avg Annual Daily Max', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = AvgYDMaxStaPr)

    for i in range(NoStation) :
        print('%-22s' % AvgYDMaxStationPr[i], '%-20s' % StationLat[i], '%-20s' % StationLon[i], file = AvgYDMaxStaPr)

    return AvgYDMaxStationPr

def MaxNation() :

    # Calculate average annual daily maxima nation-wide
    AvgYDMaxNationPrRecord = [[[0 for i in range(DataYears)] for j in range(len(DataLon))] for k in range(len(DataLat))]
    AvgYDMaxNationPr = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    count = 0
    for i in range(DataYears) :
        if ((i - 2) % 4 == 0) :
            YearLength = 366
        else :
            YearLength = 365
        for j in range(YearLength) :
            for m in range(len(DataLat)) :
                for n in range(len(DataLon)) :
                    if (j == 0) :  
                        AvgYDMaxNationPrRecord[m][n][i] = DataPr[count][m][n]
                    else :
                        if (DataPr[count][m][n] > AvgYDMaxNationPrRecord[m][n][i]) :
                            AvgYDMaxNationPrRecord[m][n][i] = DataPr[count][m][n]
            count = count + 1

    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            for k in range(DataYears) :
                AvgYDMaxNationPr[i][j] = AvgYDMaxNationPr[i][j] + AvgYDMaxNationPrRecord[i][j][k] / DataYears

    # Write average annual daily maxima nation-wide
    open('Average_Annual_Daily_Maxima_Spain.txt','w')

    AvgYDMaxNatPr = open('Average_Annual_Daily_Maxima_Spain.txt','w')

    AvgYDMaxNatPr.seek(0)
    AvgYDMaxNatPr.truncate()

    print('%-20s' % 'Avg Annual Daily Max', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = AvgYDMaxNatPr)
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            print('%-20s' % AvgYDMaxNationPr[i][j], '%-20s' % DataLat[i], '%-20s' % DataLon[j], file = AvgYDMaxNatPr)

    AvgYDMaxNatPr.close()

    return AvgYDMaxNationPr

def RatioStation() :

    # Read in data for calculation
    with open ('Average_Annual_Daily_Maxima_Station.txt') as file_object :
        lines = file_object.readlines()
    dataset = [[] for i in range(len(lines))]
    for i in range(len(dataset)):
        dataset[i][:] = (item for item in lines[i].strip().split(' '))
     
    AvgYDMaxStationPr = [0 for i in range(NoStation)]

    for i in range(NoStation) :
            if (dataset[i][0] == '0') :
                AvgYDMaxStationPr[i + 1] = 0
            else:
                AvgYDMaxStationPr[i] = float(dataset[i + 1][0])

    file_object.close()

    with open ('Average_Annual_Precipitaion_Station.txt') as file_object :
        lines = file_object.readlines()
    dataset = [[] for i in range(len(lines))]
    for i in range(len(dataset)):
        dataset[i][:] = (item for item in lines[i].strip().split(' '))
    
    AvgYYStationPr = [0 for i in range(NoStation)]

    for i in range(NoStation) :
            if (dataset[i + 1][0] == '0') :
                AvgYYStationPr[i] = 0
            else :
                AvgYYStationPr[i] = float(dataset[i + 1][0])

    file_object.close()
    
    # Calculate Maxima ratio at-sites
    MaxRatioStation = [0 for i in range(NoStation)]

    for i in range(NoStation) :
        if (AvgYYStationPr[i] == 0) :
            MaxRatioStation[i] = 0
        else :
            MaxRatioStation[i] = AvgYDMaxStationPr[i] / AvgYYStationPr[i]

    # Write Maxima ratio at-sites
    open('Maxima_Ratio_Station.txt','w')

    MaxRatioSta = open('Maxima_Ratio_Station.txt','w')

    MaxRatioSta.seek(0)
    MaxRatioSta.truncate()

    print('%-20s' % 'Maxima Ratio', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = MaxRatioSta)
    for i in range(NoStation) :
        print('%-20s' % MaxRatioStation[i], '%-20s' % StationLat[i], '%-20s' % StationLon[i], file = MaxRatioSta)

    MaxRatioSta.close()

    return MaxRatioStation

def RatioNation() :

    # Read in data for calculation
    with open ('Average_Annual_Daily_Maxima_Spain.txt') as file_object :
        lines = file_object.readlines()
    dataset = [[] for i in range(len(lines))]
    for i in range(len(dataset)):
        dataset[i][:] = (item for item in lines[i].strip().split(' '))
    
    AvgYDMaxNationPr = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    count = 0
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            if (dataset[count + 1][0] == '0') :
                AvgYDMaxNationPr[i][j] = 0
            else:
                AvgYDMaxNationPr[i][j] = float(dataset[count + 1][0])
            count = count + 1

    #file_object.close()

    with open ('Average_Annual_Precipitaion_Spain.txt') as file_object :
        lines = file_object.readlines()
    dataset = [[] for i in range(len(lines))]
    for i in range(len(dataset)):
        dataset[i][:] = (item for item in lines[i].strip().split(' '))
    
    AvgYYNationPr = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    count = 0
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            if (dataset[count + 1][0] == '0') :
                AvgYYNationPr[i][j] = 0
            else :
                AvgYYNationPr[i][j] = float(dataset[count + 1][0])
            count = count + 1

    file_object.close()

    # Calculate Maxima ratio nation-wide
    MaxRatioNation = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            if (AvgYYNationPr[i][j] == 0) :
                MaxRatioNation[i][j] = 0
            else :
                MaxRatioNation[i][j] = AvgYDMaxNationPr[i][j] / AvgYYNationPr[i][j]
    
    # Write Maxima ratio nation-wide
    open('Maxima_Ratio_Nation.txt','w')

    MaxRatioNat = open('Maxima_Ratio_Nation.txt','w')

    MaxRatioNat.seek(0)
    MaxRatioNat.truncate()

    print('%-20s' % 'Maxima Ratio', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = MaxRatioNat)
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            print('%-20s' % MaxRatioNation[i][j], '%-20s' % DataLat[i], '%-20s' % DataLon[j], file = MaxRatioNat)

    MaxRatioNat.close()

    return MaxRatioNation

def StationPr() :

    # Write Station precipitation data
    StationPr = [[0 for i in range(len(DataTime))] for j in range(NoStation)]
    Time = [0 for i in range(len(DataTime))]
    
    for i in range(NoStation) :
        for j in range(len(DataTime)) :
            Time[j] = j
            StationPr[i][j] = DataPr[j][MapLat[i]][MapLon[i]]

    open('Station_Precipitation.txt','w')

    StaPr = open('Station_Precipitation.txt','w')

    StaPr.seek(0)
    StaPr.truncate()

    print('%-20s' % 'Precipitation', '%-20s' % 'Time', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = StaPr)
    for i in range(len(DataTime)) :
        for j in range(NoStation) :
            print('%-20s' % StationPr[j][i], '%-20s' % Time[i], '%-20s' % StationLat[j], '%-20s' % StationLon[j], file = StaPr)
    
    StaPr.close()

    return StationPr

#CoorTransform()

#AvgStation()
#AvgNation()
#MaxStaion()
#MaxNation()
#RatioStation()
#RatioNation()
#StationPr()

############################################################################################################################################################
# Heatmap Plots

def PlotHeatMap() :

    # 1. Station plots
    # Read in station and location statistics
    # Longitude is x and latitude is y on the map, and in this case, epsg4326 coordinates are read in
    df = pd.DataFrame(
        {'Station': StationName,
         'Latitude': StationLat,
         'Longitude': StationLon})

    # Construct location points
    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

    # Transfer EPSG4326 coordinates to EPSG3857 coordinates
    for i in range(NoStation):
        gdf.Longitude[i],gdf.Latitude[i] = transform(P4326, P3857, gdf.Longitude[i], gdf.Latitude[i])

    gdf = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))

    # Generate the world map
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world = world.to_crs(epsg=3857)

    # Construct the country map
    ax = world[world.name == 'Spain'].plot(
        figsize=(10, 10), alpha=0.5, color='none', edgecolor='black')
    ctx.add_basemap(ax, zoom=7) # Add basemap to the plot, source=ctx.providers.Stamen.TonerLite

    # Plot the station points
    gdf.plot(ax=ax, color='red')

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    plt.savefig('Station.PNG')
    plt.show()

    # 2. Average annual precipitation plot
    # Read in data
    with open ('Average_Annual_Precipitaion_Spain.txt') as file_object :
        lines1 = file_object.readlines()
    dataset1 = [[] for i in range(len(lines1))]
    for i in range(len(dataset1)):
        dataset1[i][:] = (item for item in lines1[i].strip().split(' '))

    AvgYYNationPr = [0 for i in range(len(DataLat) * len(DataLon))]

    for i in range(len(DataLat) * len(DataLon)) :
        if (dataset1[i + 1][0] == '0') :
            AvgYYNationPr[i] = 0
        else :
            AvgYYNationPr[i] = float(dataset1[i + 1][0]) # To note that if coordinates data is read in, there should be alterations to dataset since there will be empty strings

    # Construct location points
    AvgYYPr = pd.DataFrame(
        {'Precipitation': AvgYYNationPr,
         'Latitude': EP3857DataLat,
         'Longitude': EP3857DataLon})

    gAvgYYPr = AvgYYPr.pivot_table(index='Latitude', 
                    columns='Longitude', 
                    values='Precipitation', 
                    aggfunc='mean')
    ax = seaborn.heatmap(gAvgYYPr,
                        cmap = "YlGnBu", 
                        vmin = 1,
                        zorder = 1,
                        annot_kws = {'alpha':0.8}
                        )
    ax.invert_yaxis()

    # Add basemap to the plot
    ctx.add_basemap(ax, zoom=7)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    plt.savefig('Average_Annual_Precipitation_Heatmap.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
    plt.show()
    plt.close()

    # 3. Average annual daily maxima precipitation plot
    # Read in data
    with open ('Average_Annual_Daily_Maxima_Spain.txt') as file_object :
        lines2 = file_object.readlines()
    dataset2 = [[] for i in range(len(lines2))]
    for i in range(len(dataset2)):
        dataset2[i][:] = (item for item in lines2[i].strip().split(' '))

    AvgYDMaxNationPr = [0 for i in range(len(DataLat) * len(DataLon))]

    for i in range(len(DataLat)* len(DataLon)) :
        if (dataset2[i + 1][0] == '0') :
            AvgYDMaxNationPr[i] = 0
        else :
            AvgYDMaxNationPr[i] = float(dataset2[i + 1][0])

    # Construct location points
    AvgYDPr = pd.DataFrame(
        {'Precipitation': AvgYDMaxNationPr,
         'Latitude': EP3857DataLat,
         'Longitude': EP3857DataLon})

    gAvgYDPr = AvgYDPr.pivot_table(index='Latitude', 
                    columns='Longitude', 
                    values='Precipitation', 
                    aggfunc='mean')

    ax = seaborn.heatmap(gAvgYDPr, cmap="YlGnBu", vmin=1, annot_kws={'alpha':0.8})
    ax.invert_yaxis()

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    # Add basemap to the plot
    ctx.add_basemap(ax, zoom=7)

    plt.savefig('Average_Annual_Daily_Maxima_Heatmap.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
    plt.show()
    plt.close()

    # 4. Average annual daily maxima / annual precipitation plot
    # Read in data
    with open ('Maxima_Ratio_Nation.txt') as file_object :
        lines3 = file_object.readlines()
    dataset3 = [[] for i in range(len(lines3))]
    for i in range(len(dataset3)):
        dataset3[i][:] = (item for item in lines3[i].strip().split(' '))

    MaxRatioNation = [0 for i in range(len(DataLat) * len(DataLon))]

    for i in range(len(DataLat) * len(DataLon)) :
        if (dataset3[i + 1][0] == '0') :
            MaxRatioNation[i] = 0
        else :
            MaxRatioNation[i] = float(dataset3[i + 1][0])

    # Construct location points
    MaxRatio = pd.DataFrame(
        {'Ratio': MaxRatioNation,
         'Latitude': EP3857DataLat,
         'Longitude': EP3857DataLon})

    gMaxRatio = MaxRatio.pivot_table(index='Latitude', 
                    columns='Longitude', 
                    values='Ratio', 
                    aggfunc='mean')
    
    ax = seaborn.heatmap(gMaxRatio, cmap="YlGnBu", vmin=0, vmax=0.2, annot_kws={'alpha':0.8})
    ax.invert_yaxis()

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    # Add basemap to the plot
    ctx.add_basemap(ax, zoom=7)

    plt.savefig('Maxima_Ratio_Heatmap.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
    plt.show()
    plt.close()

#PlotHeatMap()

###################
# Gaussian Knenel Spatial Interpolation Plots

###################
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
area = world[world.name == 'Spain']

latlng_bounds = area.total_bounds
area = area.to_crs(epsg = 3857)
axis = area.total_bounds

max_tiles = 10

# Create the map stretching over the requested area
ax = area.plot(alpha = 0)

def add_basemap(ax, latlng_bounds, axis, url='https://a.basemaps.cartocdn.com/light_all/tileZ/tileX/tileY@2x.png') :
    prev_ax = ax.axis()
    # TODO: Zoom should surely take output pixel request size into account...
    zoom = ctx.tile._calculate_zoom(*latlng_bounds)
    while ctx.tile.howmany(*latlng_bounds, zoom, ll=True) > max_tiles:      # dont ever try to download loads of tiles
        zoom = zoom - 1
    print("downloading %d tiles with zoom level %d" % (ctx.tile.howmany(*latlng_bounds, zoom, ll=True), zoom))
    basemap, extent = ctx.bounds2img(*axis, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    ax.axis(prev_ax)        # restore axis after changing the background
###################

def GaussianInterpolationPlot() :

    # 1. Average annual precipitation plot
    # Read in data
    with open ('Average_Annual_Precipitaion_Spain.txt') as file_object :
        lines1 = file_object.readlines()
    dataset1 = [[] for i in range(len(lines1))]
    for i in range(len(dataset1)):
        dataset1[i][:] = (item for item in lines1[i].strip().split(' '))

    AvgYYNationPr = [0 for i in range(len(DataLat) * len(DataLon))]

    for i in range(len(DataLat) * len(DataLon)) :
        if (dataset1[i + 1][0] == '0') :
            AvgYYNationPr[i] = 0
        else :
            AvgYYNationPr[i] = float(dataset1[i + 1][0]) # To note that if coordinates data is read in, there should be alterations to dataset since there will be empty strings

    # Construct location points
    AvgYYPr = pd.DataFrame(
        {'Precipitation': AvgYYNationPr,
         'Latitude': EP3857DataLat,
         'Longitude': EP3857DataLon})

    #gAvgYYPr = geopandas.GeoDataFrame(
        #AvgYYPr, geometry=geopandas.points_from_xy(AvgYYPr.Longitude, AvgYYPr.Latitude))

    # Create the map stretching over the requested area
    ax = area.plot(alpha = 0)

    # Calculate the KDE
    data = np.c_[AvgYYPr.Longitude, AvgYYPr.Latitude]
    kde = scipy.stats.gaussian_kde(data.T, bw_method = "scott", weights = AvgYYPr.Precipitation)
    data_std = data.std(axis = 0, ddof = 1)
    bw_x = getattr(kde, "scotts_factor")() * data_std[0]
    bw_y = getattr(kde, "scotts_factor")() * data_std[1]
    grid_x = grid_y = 100
    x_support = seaborn.utils._kde_support(data[:, 0], bw_x, grid_x, 3, (axis[0], axis[2]))
    y_support = seaborn.utils._kde_support(data[:, 1], bw_y, grid_y, 3, (axis[1], axis[3]))
    xx, yy = np.meshgrid(x_support, y_support)
    levels = kde([xx.ravel(), yy.ravel()]).reshape(xx.shape)

    cset = ax.contourf(xx, yy, levels,
        50, # n_levels
 
        cmap = seaborn.palettes.blend_palette(('#ffffff10', '#ff0000af'), 6, as_cmap = True),
        antialiased = True,       # avoids lines on the contours to some extent
    )
    #plt.colorbar(cset)

    # Hide lowest N levels
    for i in range(0,5):
        cset.collections[i].set_alpha(0)
    for i in range(5,43) :
        cset.collections[i].set_alpha(0.6)

    # Add basemap to the plot
    add_basemap(ax, latlng_bounds, axis)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
 
    plt.savefig('Average_Annual_Precipitation_Gaussian.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)

    # 2. Average annual daily maxima precipitation plot
    # Read in data
    with open ('Average_Annual_Daily_Maxima_Spain.txt') as file_object :
        lines2 = file_object.readlines()
    dataset2 = [[] for i in range(len(lines2))]
    for i in range(len(dataset2)):
        dataset2[i][:] = (item for item in lines2[i].strip().split(' '))

    AvgYDMaxNationPr = [0 for i in range(len(DataLat) * len(DataLon))]

    for i in range(len(DataLat) * len(DataLon)) :
        if (dataset2[i + 1][0] == '0') :
            AvgYDMaxNationPr[i] = 0
        else :
            AvgYDMaxNationPr[i] = float(dataset2[i + 1][0])

    # Construct location points
    AvgYDPr = pd.DataFrame(
        {'Precipitation': AvgYDMaxNationPr,
         'Latitude': EP3857DataLat,
         'Longitude': EP3857DataLon})

    #gAvgYDPr = geopandas.GeoDataFrame(
        #AvgYDPr, geometry=geopandas.points_from_xy(AvgYDPr.Longitude, AvgYDPr.Latitude))

    # Create the map stretching over the requested area
    ax = area.plot(alpha = 0)

    # Calculate the KDE
    data = np.c_[AvgYDPr.Longitude, AvgYDPr.Latitude]
    kde = scipy.stats.gaussian_kde(data.T, bw_method = "scott", weights = AvgYDPr.Precipitation)
    data_std = data.std(axis = 0, ddof = 1)
    bw_x = getattr(kde, "scotts_factor")() * data_std[0]
    bw_y = getattr(kde, "scotts_factor")() * data_std[1]
    grid_x = grid_y = 100
    x_support = seaborn.utils._kde_support(data[:, 0], bw_x, grid_x, 3, (axis[0], axis[2]))
    y_support = seaborn.utils._kde_support(data[:, 1], bw_y, grid_y, 3, (axis[1], axis[3]))
    xx, yy = np.meshgrid(x_support, y_support)
    levels = kde([xx.ravel(), yy.ravel()]).reshape(xx.shape)

    cset = ax.contourf(xx, yy, levels,
       50, # n_levels
    
       cmap = seaborn.palettes.blend_palette(('#ffffff10', '#ff0000af'), 6, as_cmap = True),
       antialiased = True,       # avoids lines on the contours to some extent
    )
    plt.colorbar(cset)

    # Hide lowest N levels
    for i in range(0,5) :
        cset.collections[i].set_alpha(0)
    for i in range(5,43) :
        cset.collections[i].set_alpha(0.6)

    # Add basemap to the plot
    add_basemap(ax, latlng_bounds, axis)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
 
    plt.savefig('Average_Annual_Daily_Maxima_Gaussian.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)

    # 3. Average annual daily maxima / annual precipitation plot
    # Read in data
    with open ('Maxima_Ratio_Nation.txt') as file_object :
        lines3 = file_object.readlines()
    dataset3 = [[] for i in range(len(lines3))]
    for i in range(len(dataset3)):
        dataset3[i][:] = (item for item in lines3[i].strip().split(' '))

    MaxRatioNation = [0 for i in range(len(DataLat) * len(DataLon))]

    for i in range(len(DataLat) * len(DataLon)) :
        if (dataset3[i + 1][0] == '0') :
            MaxRatioNation[i] = 0
        else :
            MaxRatioNation[i] = float(dataset3[i + 1][0])

    # Construct location points
    MaxRatio = pd.DataFrame(
        {'Ratio': MaxRatioNation,
         'Latitude': EP3857DataLat,
         'Longitude': EP3857DataLon})

    #gMaxRatio = geopandas.GeoDataFrame(
        #MaxRatio, geometry=geopandas.points_from_xy(MaxRatio.Longitude, MaxRatio.Latitude))

    # Create the map stretching over the requested area
    ax = area.plot(alpha = 0)

    # Calculate the KDE
    data = np.c_[MaxRatio.Longitude, MaxRatio.Latitude]
    kde = scipy.stats.gaussian_kde(data.T, bw_method = "scott", weights = MaxRatio.Ratio)
    data_std = data.std(axis = 0, ddof = 1)
    bw_x = getattr(kde, "scotts_factor")() * data_std[0]
    bw_y = getattr(kde, "scotts_factor")() * data_std[1]
    grid_x = grid_y = 100
    x_support = seaborn.utils._kde_support(data[:, 0], bw_x, grid_x, 3, (axis[0], axis[2]))
    y_support = seaborn.utils._kde_support(data[:, 1], bw_y, grid_y, 3, (axis[1], axis[3]))
    xx, yy = np.meshgrid(x_support, y_support)
    levels = kde([xx.ravel(), yy.ravel()]).reshape(xx.shape)

    cset = ax.contourf(xx, yy, levels,
        50, # n_levels
 
        cmap = seaborn.palettes.blend_palette(('#ffffff10', '#ff0000af'), 6, as_cmap = True),
        antialiased = True,       # avoids lines on the contours to some extent
    )
    #plt.colorbar(cset)

    # Hide lowest N levels
    for i in range(0,5):
        cset.collections[i].set_alpha(0)
    for i in range(5,43) :
        cset.collections[i].set_alpha(0.6)

    # Add basemap to the plot
    add_basemap(ax, latlng_bounds, axis)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
 
    plt.savefig('Maxima_Ratio_Gaussian.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)

#GaussianInterpolationPlot()

############################################################################################################################################################
# Extreme Value Analysis

# Calculation functions
# sum from sample (t+1) to maximum
def sumt(data,t) :

    sum = 0
    for i in range(len(data) - t - 1) :
        sum = sum + data[len(data) - 1 - i]
    return sum

# Calculate sum of list1i * list2i
def sumxy(list1,list2) :
    result = 0

    if (len(list1) != len(list2)) :
        return print('not even list')
    else :
        for i in range(len(list1)) :
            result = result + list1[i] * list2[i]
        return result

# Return N largest elements of the list
def NMaxElements(triallist, N) :
    final_list = [] 
    
    triallist.sort()

    for i in range(0, N):  
        final_list.append(triallist[len(triallist) - N + i])
    
    return final_list

# Return N threshold
def NThreshold(triallist,N) :
    triallist.sort()

    return triallist[len(triallist) - N - 1]

# Calculate beta0
def Calbeta0(triallist) :
    beta0 = 0

    for i in range(len(triallist)) :
        beta0 = beta0 + triallist[i] / len(triallist)
    
    return beta0

# Calculate beta1
def Calbeta1(triallist) :
    beta1 = 0

    for i in range(len(triallist)) :
        beta1 = beta1 + (len(triallist) - i - 1) * triallist[i] / (len(triallist) * (len(triallist) - 1))

    return beta1

# Return PPWR2 value
def PPWCCValue(triallist, alpha, kappa) :

    yI = [0 for i in range(len(triallist))]
    hatyI = [0 for i in range(len(triallist))]
    EmpCDF = [0 for i in range(len(triallist))]
    omega = [0 for i in range(len(triallist))]
    numerator = denominator1 = denominator2 = 0
    bary = barhaty = PPWR2 = 0
    n = len(triallist)
    
    for i in range(n) :
        yI[i] = triallist[i]
        EmpCDF[i] = (i + 1 - 0.15) / n
        omega[i] = 1 / (1 - EmpCDF[i])
        hatyI[i] = alpha * (1 - (1 - EmpCDF[i]) ** kappa) / kappa
    
    bary = sumxy(yI, omega) / (n * sum(omega))
    barhaty = sumxy(hatyI, omega) / (n * sum(omega))
    
    if (n == 1) :
        PPWR2 = 1
    else :
        for i in range(n) :
            numerator = numerator + (yI[i] * hatyI[i] - n * bary * barhaty) * omega[i]
            denominator1 = denominator1 + (yI[i] ** 2 - n * bary ** 2) * omega[i]
            denominator2 = denominator2 + (hatyI[i] ** 2 - n * barhaty ** 2) * omega[i]
        numerator = numerator ** 2
    
        PPWR2 = numerator / (denominator1 * denominator2)

    return PPWR2

# A) Distribution parameters fitting

# Fit station precipitation data to GP(Generalized Pareto) Distribution and find distribution parameter
# In this case, we study the tail behavior of extreme values over the threshold (xi,n - xk,n)

# CDF of GPD: F(x) = 1 - (1 - k * x / alpha) ^ (1 / k)
# pdf of GPD: f(x) = (1 - k * x / alpha) ^ (1 / k - ) / alpha

# Using the method of PWM(probability-weighted moments)
# scale parameter:alpha = 2 * beta0 * beta1 / (beta0 - 2 * beta1)
# shape paramter: k = beta0 / (beta0 - 2 * beta1) - 2
# beta0 = (x1,n + x2,n + x3,n + ... + xn,n) /n
# beta1 = ((n-1) * x1,n + (n-2) * x2,n + ... + x(n-1),n + 0) / (n * (n - 1))

###############################
def ParameterFit() :

    # Read in station precipitation data
    with open ('Station_Precipitation.txt') as file_object :
        lines4 = file_object.readlines()
    dataset4 = [[] for i in range(len(lines4))]
    for i in range(len(dataset4)):
        dataset4[i][:] = (item for item in lines4[i].strip().split(' '))

    StationPr = [[0 for i in range(len(DataTime))] for j in range(NoStation)]

    count = 0
    for i in range(len(DataTime)) :
        for j in range(NoStation) :
            if (dataset4[count + 1][0] == '0') :
                StationPr[j][i] = 0
            else :
                StationPr[j][i] = float(dataset4[count + 1][0])
            count = count + 1

    # Take extreme precipitaiton of largest 1200 values
    NoExtreme = 1200
    ExStationPr = [[0 for i in range(NoExtreme)] for j in range(NoStation)]
    Ithreshold = [0 for i in range(NoStation)]

    for i in range(NoStation) :
        ExStationPr[i][:] = NMaxElements(StationPr[i][:], NoExtreme)

    for i in range(NoStation) :
        Ithreshold[i] = NThreshold(StationPr[i][:], NoExtreme)
        for j in range(NoExtreme) :
            ExStationPr[i][j] = ExStationPr[i][j] - Ithreshold[i]

    # Calculate distribution parameters
    beta0 = [0 for i in range(NoStation)]
    beta1 = [0 for i in range(NoStation)]

    alpha = [0 for i in range(NoStation)]
    kappa = [0 for i in range(NoStation)]

    for i in range(NoStation) :
        beta0[i] = Calbeta0(ExStationPr[i][:])
        beta1[i] = Calbeta1(ExStationPr[i][:])
    
        # There are points where data not recorded
        if (beta0[i] == 0 and beta1[i] == 0) :
            beta0[i] = 0
            beta1[i] = 0
            alpha[i] = 0
            kappa[i] = 0
        else :
            alpha[i] = 2 * beta0[i] * beta1[i] / (beta0[i] - 2 * beta1[i])
            kappa[i] = beta0[i] / (beta0[i] - 2 * beta1[i]) - 2

    # Write distribution parameters
    open('Station_Parameters.txt','w')

    StaPar = open('Station_Parameters.txt','w')

    StaPar.seek(0)
    StaPar.truncate()

    print('%-20s' % 'Station', '%-20s' % 'Alpha', '%-20s' % 'Kappa', '%-20s' % 'Threshold', '%-20s' % 'Latitude', '%-20s' % 'Longitude', file = StaPar)

    for i in range(NoStation) :
        print('%-20s' % StationName[i], '%-20s' % alpha[i], '%-20s' % kappa[i], '%-20s' % Ithreshold[i], '%-20s' % StationLat[i], '%-20s' % StationLon[i], file = StaPar)
    StaPar.close()

#ParameterFit()

# B) Analysis the data series

# 1. Return period

# 2. Mean excess plot and probability plot–weighted correlation coefficient plot (Access the validity of the GP assumption)

# Mean Excess plot/its regression and PPWCC plot
def ExaminePlot(i, triallist, alpha, kappa) :

    if (alpha != 0 and kappa != 0) :
        
        # Mean Excess plot with omitted tails/its regression

        length = len(triallist) - 1
        t = [0 for i in range(length)]
        e = [0 for i in range(length)]
        reg_e = [0 for i in range(length)]
        yI = [0 for i in range(len(triallist))]
        PPWR2 = [0 for i in range(len(triallist))]

        for i in range(length) :
            t[i] = triallist[i]
            e[i] = sumt(triallist,i) / (len(triallist) - i - 1) - triallist[i]

        fig, ax1 = plt.subplots()

        ax1.scatter(t, e, color = 'black', s = 5)
        ax1.plot(t, e, color = 'black', label = 'empirical mean excess')
        slope,intercept,_,_,_ = scipy.stats.linregress(t,e)
        for i in range(length) :
            reg_e[i] = intercept + t[i] * slope
        ax1.plot(t, reg_e, color = 'red', label = 'regression plot')
        ax1.set_xlabel('x')
        ax1.set_ylabel('e(x)')
        plt.legend()

        # Probability plot–weighted correlation coefficient(PPWCC) plot
    
        i = 0
        while (len(triallist) > 0) :
            yI[i] = triallist[0]
            PPWR2[i] = PPWCCValue(triallist, alpha, kappa)
            triallist.remove(triallist[0])
            i = i + 1
    
        ax2 = ax1.twinx()

        ax2.scatter(yI, PPWR2, color = 'blue', s = 5)
        ax2.plot(yI, PPWR2, color = 'blue', label = 'PPWCC plot')
        ax2.set_ylabel('PPWCC2')
        plt.legend()

        fig.tight_layout()

# Mean Excess plot with omitted tails/its regression and PPWCC plot
def ExaminePlotOmit(i, triallist, omit, alpha, kappa) :
    
    if (alpha != 0 and kappa != 0) :
        
        # Mean Excess plot with omitted tails/its regression

        length = len(triallist) - omit
        t = [0 for i in range(length)]
        e = [0 for i in range(length)]
        reg_e = [0 for i in range(length)]
        yI = [0 for i in range(length)]
        PPWR2 = [0 for i in range(length)]

        for i in range(length) :
            t[i] = triallist[i]
            e[i] = sumt(triallist,i) / (len(triallist) - i - 1) - triallist[i]

        fig, ax1 = plt.subplots()

        ax1.scatter(t, e, color = 'black', s = 5)
        ax1.plot(t, e, color = 'black', label = 'empirical mean excess')
        slope,intercept,_,_,_ = scipy.stats.linregress(t,e)
        for i in range(length) :
            reg_e[i] = intercept + t[i] * slope
        ax1.plot(t, reg_e, color = 'red', label = 'regression plot')
        ax1.set_xlabel('t')
        ax1.set_ylabel('e(t)')
        plt.legend()

        # Probability plot–weighted correlation coefficient(PPWCC) plot
    
        i = 0
        while (len(triallist) > omit) :
            yI[i] = triallist[0]
            PPWR2[i] = PPWCCValue(triallist, alpha, kappa)
            triallist.remove(triallist[0])
            i = i + 1
    
        ax2 = ax1.twinx()

        ax2.scatter(yI, PPWR2, color = 'blue', s = 5)
        ax2.plot(yI, PPWR2, color = 'blue', label = 'PPWCC plot')
        ax2.set_ylabel('PPWCC2')
        plt.legend()

        fig.tight_layout()

###############################

def DataExaminePlot() :
    
    # Read in station precipitation data
    with open ('Station_Precipitation.txt') as file_object :
        lines4 = file_object.readlines()
    dataset4 = [[] for i in range(len(lines4))]
    for i in range(len(dataset4)):
        dataset4[i][:] = (item for item in lines4[i].strip().split(' '))

    StationPr = [[0 for i in range(len(DataTime))] for j in range(NoStation)]

    count = 0
    for i in range(len(DataTime)) :
        for j in range(NoStation) :
            if (dataset4[count + 1][0] == '0') :
                StationPr[j][i] = 0
            else :
                StationPr[j][i] = float(dataset4[count + 1][0])
            count = count + 1
    
    # Read in Station Paramter, alpha, kappa
    with open ('Station_Parameters.txt') as file_object :
        lines5 = file_object.readlines()
    dataset5 = [[] for i in range(len(lines5))]
    dataset05 = [[] for i in range(len(lines5))]
    for i in range(len(dataset05)):
        dataset05[i][:] = (item for item in lines5[i].strip().split(' '))
    
    # Delete invalid data caused by space
    for i in range(len(lines5)) :
        for j in range(len(dataset05[i])) :
            if dataset05[i][j] == '' :
                continue
            else :
                dataset5[i].append(dataset05[i][j])
    
    alpha = [0 for i in range(NoStation)]
    kappa = [0 for i in range(NoStation)]

    for i in range(NoStation) :
        if (dataset5[i + 1][1] == '0') :
            alpha[i] = 0
            kappa[i] = 0
        else :
            alpha[i] = float(dataset5[i + 1][1])
            kappa[i] = float(dataset5[i + 1][2])

    # Take extreme precipitaiton of largest 1200 values
    NoExtreme = 1200
    omit = int(0.05 * NoExtreme) # omit largest 5 percent data
    ExStationPr = [[0 for i in range(NoExtreme)] for j in range(NoStation)]

    for i in range(NoStation) :
        ExStationPr[i][:] = NMaxElements(StationPr[i][:], NoExtreme)

    for i in range(NoStation) :
        Ithreshold = NThreshold(StationPr[i][:], NoExtreme)
        for j in range(NoExtreme) :
            ExStationPr[i][j] = ExStationPr[i][j] - Ithreshold
    
    # Write omitted stations
    open('Station Precipitation Extreme Values Examination (Mean Excess Plot and PPWCC)/Omit_Station.txt','w')

    Osta = open('Station Precipitation Extreme Values Examination (Mean Excess Plot and PPWCC)/Omit_Station.txt','w')

    Osta.seek(0)
    Osta.truncate()
    
    for i in range(NoStation) :

        if (alpha[i] == 0 and kappa[i] == 0) :
            print('Station', int(i + 1), 'Omitted', file = Osta)
            
    Osta.close()

    # Plot Mean Excess Plots for every stations' extreme values
    for i in range(NoStation) :

        #ExaminePlot(i, ExStationPr[i][:], alpha[i], kappa[i])
        ExaminePlotOmit(i, ExStationPr[i][:], omit, alpha[i], kappa[i]) # Omit largest few data to make mean excess plot better-looking
        
        if (alpha[i] != 0 or kappa[i] != 0) :
            plt.savefig('Station Precipitation Extreme Values Examination (Mean Excess Plot and PPWCC)/Plot_'+StationName[i]+'.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
            plt.close()

#DataExaminePlot()

# C) Examine the goodness of fit

# 1. Probability plots (PP) (y-haty)
def ProPlot() :

    # Read in station precipitation data
    with open ('Station_Precipitation.txt') as file_object :
        lines4 = file_object.readlines()
    dataset4 = [[] for i in range(len(lines4))]
    for i in range(len(dataset4)):
        dataset4[i][:] = (item for item in lines4[i].strip().split(' '))

    StationPr = [[0 for i in range(len(DataTime))] for j in range(NoStation)]

    count = 0
    for i in range(len(DataTime)) :
        for j in range(NoStation) :
            if (dataset4[count + 1][0] == '0') :
                StationPr[j][i] = 0
            else :
                StationPr[j][i] = float(dataset4[count + 1][0])
            count = count + 1
    
    # Read in Station Paramter, alpha, kappa
    with open ('Station_Parameters.txt') as file_object :
        lines5 = file_object.readlines()
    dataset5 = [[] for i in range(len(lines5))]
    dataset05 = [[] for i in range(len(lines5))]
    for i in range(len(dataset05)):
        dataset05[i][:] = (item for item in lines5[i].strip().split(' '))
    
    # Delete invalid data caused by space
    for i in range(len(lines5)) :
        for j in range(len(dataset05[i])) :
            if dataset05[i][j] == '' :
                continue
            else :
                dataset5[i].append(dataset05[i][j])
    
    alpha = [0 for i in range(NoStation)]
    kappa = [0 for i in range(NoStation)]

    for i in range(NoStation) :
        if (dataset5[i + 1][1] == '0') :
            alpha[i] = 0
            kappa[i] = 0
        else :
            alpha[i] = float(dataset5[i + 1][1])
            kappa[i] = float(dataset5[i + 1][2])

    # Take extreme precipitaiton of largest 1200 values
    NoExtreme = 1200
    ExStationPr = [[0 for i in range(NoExtreme)] for j in range(NoStation)]

    for i in range(NoStation) :
        ExStationPr[i][:] = NMaxElements(StationPr[i][:], NoExtreme)

    for i in range(NoStation) :
        Ithreshold = NThreshold(StationPr[i][:], NoExtreme)
        for j in range(NoExtreme) :
            ExStationPr[i][j] = ExStationPr[i][j] - Ithreshold

     # Write omitted stations
    open('Probability Plots/Omit_Station.txt','w')

    PPOsta = open('Probability Plots/Omit_Station.txt','w')

    PPOsta.seek(0)
    PPOsta.truncate()
    
    for i in range(NoStation) :

        if (alpha[i] == 0 and kappa[i] == 0) :
            print('Station', int(i + 1), 'Omitted', file = PPOsta)
            
    PPOsta.close()       
    
    # Probability Plot
    for i in range(NoStation) :
        
        if (alpha[i] != 0 and kappa[i] != 0) :
            # Calculate PP values
            n = len(ExStationPr[i][:])
            yI = [0 for i in range(n)]
            hatyI = [0 for i in range(n)]
            EmpCDF = [0 for i in range(n)]
            omega = [0 for i in range(n)]
            reg_yI = [0 for i in range(n)]

            for j in range(n):
                yI[j] = ExStationPr[i][j]
                EmpCDF[j] = (j + 1 - 0.15) / n
                omega[j] = 1 / (1 - EmpCDF[j])
                hatyI[j] = alpha[i] * (1 - (1 - EmpCDF[j]) ** kappa[i]) / kappa[i]
            
            ax = plt.subplot()
            # PP points, plot and regression
            ax.scatter(yI, hatyI, color = 'black', s = 5)
            ax.plot(yI, hatyI, color = 'black', label = 'Probability Plot')
            slope,intercept,_,_,_ = scipy.stats.linregress(yI, hatyI)
            for k in range(n) :
                reg_yI[k] = intercept + yI[k] * slope
            ax.plot(yI, reg_yI, color = 'red', label = 'Regression Plot')
            ax.plot(yI, yI, color = 'blue', label = 'Perfect Probability Plot')
            plt.xlabel('y')
            plt.ylabel(r'$\hat{y}$')
            plt.legend()

            plt.savefig('Probability Plots/Probability Plot_'+StationName[i]+'.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
            plt.close()

#ProPlot()

# 2. a) Probability plot–weighted mean bias error (PPWMBE)
def CalPPWMBE(triallist, alpha, kappa) :
    n = len(triallist)
    yI = [0 for i in range(n)]
    hatyI = [0 for i in range(n)]
    EmpCDF = [0 for i in range(n)]
    omega = [0 for i in range(n)]

    for i in range(n):
        yI[i] = triallist[i]
        EmpCDF[i] = (i + 1 - 0.15) / n
        omega[i] = 1 / (1 - EmpCDF[i])
        hatyI[i] = alpha * (1 - (1 - EmpCDF[i]) ** kappa) / kappa
    
    PPWMBE = 0
    for i in range(n) :
        PPWMBE = PPWMBE + (hatyI[i] - yI[i]) * omega[i] / (n * sum(omega))

    return PPWMBE

#    b) Probability plot–weighted root-mean-square error (PPWRMSE)
def CalPPWRMSE(triallist, alpha, kappa) :
    n = len(triallist)
    yI = [0 for i in range(n)]
    hatyI = [0 for i in range(n)]
    EmpCDF = [0 for i in range(n)]
    omega = [0 for i in range(n)]

    for i in range(n):
        yI[i] = triallist[i]
        EmpCDF[i] = (i + 1 - 0.15) / n
        omega[i] = 1 / (1 - EmpCDF[i])
        hatyI[i] = alpha * (1 - (1 - EmpCDF[i]) ** kappa) / kappa
    
    PPWRMSE = 0
    for i in range(n) :
        PPWRMSE = PPWRMSE + omega[i] * (hatyI[i] - yI[i]) ** 2 / (n * sum(omega))

    PPWRMSE = math.sqrt(PPWRMSE)

    return PPWRMSE

#    c) Probability plot–weighted correlation coefficient(PPWCC)
# define previously as PPWCCValue function

def GoodnessOfFit() :

    # Read in station precipitation data
    with open ('Station_Precipitation.txt') as file_object :
        lines4 = file_object.readlines()
    dataset4 = [[] for i in range(len(lines4))]
    for i in range(len(dataset4)):
        dataset4[i][:] = (item for item in lines4[i].strip().split(' '))

    StationPr = [[0 for i in range(len(DataTime))] for j in range(NoStation)]

    count = 0
    for i in range(len(DataTime)) :
        for j in range(NoStation) :
            if (dataset4[count + 1][0] == '0') :
                StationPr[j][i] = 0
            else :
                StationPr[j][i] = float(dataset4[count + 1][0])
            count = count + 1
    
    # Read in Station Paramter, alpha, kappa
    with open ('Station_Parameters.txt') as file_object :
        lines5 = file_object.readlines()
    dataset5 = [[] for i in range(len(lines5))]
    dataset05 = [[] for i in range(len(lines5))]
    for i in range(len(dataset05)):
        dataset05[i][:] = (item for item in lines5[i].strip().split(' '))
    
    # Delete invalid data caused by space
    for i in range(len(lines5)) :
        for j in range(len(dataset05[i])) :
            if dataset05[i][j] == '' :
                continue
            else :
                dataset5[i].append(dataset05[i][j])
    
    alpha = [0 for i in range(NoStation)]
    kappa = [0 for i in range(NoStation)]

    for i in range(NoStation) :
        if (dataset5[i + 1][1] == '0') :
            alpha[i] = 0
            kappa[i] = 0
        else :
            alpha[i] = float(dataset5[i + 1][1])
            kappa[i] = float(dataset5[i + 1][2])

    # Take extreme precipitaiton of largest 1200 values
    NoExtreme = 1200
    ExStationPr = [[0 for i in range(NoExtreme)] for j in range(NoStation)]

    for i in range(NoStation) :
        ExStationPr[i][:] = NMaxElements(StationPr[i][:], NoExtreme)

    for i in range(NoStation) :
        Ithreshold = NThreshold(StationPr[i][:], NoExtreme)
        for j in range(NoExtreme) :
            ExStationPr[i][j] = ExStationPr[i][j] - Ithreshold

    PPWMBE = [0 for i in range(NoStation)]
    PPWRMSE = [0 for i in range(NoStation)]
    PPWCC = [0 for i in range(NoStation)]

    # Calculate goodness of fit at each station
    for i in range(NoStation) :
        if (alpha[i] == 0 and kappa[i] == 0) :
            PPWMBE[i] = 0
            PPWRMSE[i] = 0
            PPWCC[i] = 0
        else :
            PPWMBE[i] = CalPPWMBE(ExStationPr[i][:], alpha[i], kappa[i])
            PPWRMSE[i] = CalPPWRMSE(ExStationPr[i][:], alpha[i], kappa[i])
            PPWCC[i] = PPWCCValue(ExStationPr[i][:], alpha[i], kappa[i])

    # Write goodness of fit data
    open('Goodness of Fit data.txt','w')

    GOFD = open('Goodness of Fit data.txt','w')

    GOFD.seek(0)
    GOFD.truncate()

    print('%-20s' % 'Station', '%-20s' % 'PPWMBE', '%-20s' % 'PPWRMSE', '%-20s' % 'PPWCC', file = GOFD)

    for i in range(NoStation) :
        print('%-20s' % StationName[i], '%-20s' % PPWMBE[i], '%-20s' % PPWRMSE[i], '%-20s' % PPWCC[i], file = GOFD)

    GOFD.close()

#GoodnessOfFit()

#########################################################################################################################################################################################
# Spatial Probability Distribution (Extreme Value Prediction)

# Calculate x1 * y1 + x2 * y2 + x3 * y3 + ...
def prosum(xlist, ylist) :
    prosum = 0
    if (len(xlist) != len(ylist)) :
        print('Length error!!!')
    else :
        for i in range(len(xlist)) :
            prosum = prosum + xlist[i] * ylist[i]
    
    return prosum

# Create independent variables maps
def InVariableMap(DataElevation) :

    TrendSurface1 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    TrendSurface2 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanElevation = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanRelief = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    Barrier = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    # 1) The first order of Trend surface (latitude + longitude)
    # Read in epsg32630 coordinates
    with open ('Data_EP32630_Coordinates.txt') as file_object :
        lines7 = file_object.readlines()
    dataset7 = [[] for i in range(len(lines7))]
    dataset07 = [[] for i in range(len(lines7))]
    for i in range(len(dataset07)):
        dataset07[i][:] = (item for item in lines7[i].strip().split(' '))
    
    # Delete invalid data caused by space
    for i in range(len(lines7)) :
        for j in range(len(dataset07[i])) :
            if dataset07[i][j] == '' :
                continue
            else :
                dataset7[i].append(dataset07[i][j])

    UTMDataLat = [0 for i in range(len(DataLat))]
    UTMDataLon = [0 for i in range(len(DataLon))]

    count = 1
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            if (i == 0) :
                UTMDataLon[j] = float(dataset7[count][1])
            if (j == 0) :
                UTMDataLat[i] = float(dataset7[count][0])
            count = count + 1

    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            TrendSurface1[i][j] = UTMDataLat[i] + UTMDataLon[j]

    # 2) The second order of Trend surface ((latitude + longitude)^2)
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            TrendSurface2[i][j] = (UTMDataLat[i] + UTMDataLon[j]) ** 2

    # 3) Mean elevation (in the circle of 0.2 degree)
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            if (i == 0 and j == 0) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i + 1][j] + DataElevation[i][j + 1]) / 3
            elif (i == 0 and j == len(DataLon) - 1) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i + 1][j] + DataElevation[i][j - 1]) / 3
            elif (i == len(DataLat) - 1 and j == 0) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i - 1][j] + DataElevation[i][j + 1]) / 3
            elif (i == len(DataLat) - 1 and j == len(DataLon) - 1) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i - 1][j] + DataElevation[i][j - 1]) / 3
            elif (i == 0) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i + 1][j] + DataElevation[i][j - 1] + DataElevation[i][j + 1]) / 4
            elif (i == len(DataLat) - 1) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i - 1][j] + DataElevation[i][j - 1] + DataElevation[i][j + 1]) / 4
            elif (j == 0) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i - 1][j] + DataElevation[i + 1][j] + DataElevation[i][j + 1]) / 4
            elif (j == len(DataLon) - 1) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i - 1][j] + DataElevation[i + 1][j] + DataElevation[i][j - 1]) / 4
            elif (i == 1 or i == len(DataLat) - 2 or j == 1 or j ==len(DataLon) - 2) :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i + 1][j] + DataElevation[i - 1][j] + DataElevation[i][j + 1] + DataElevation[i][j - 1]) / 5
            else :
                MeanElevation[i][j] = (DataElevation[i][j] + DataElevation[i + 1][j] + DataElevation[i + 2][j] + DataElevation[i - 1][j] + DataElevation[i - 2][j] + DataElevation[i][j + 1] + DataElevation[i][j + 2] + DataElevation[i][j - 1] + DataElevation[i][j - 2] + DataElevation[i + 1][j + 1] + DataElevation[i + 1][j - 1] + DataElevation[i - 1][j + 1] + DataElevation[i - 1][j - 1]) / 13

    # 4) Mean eelief (in the circle of 0.2 degree)
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            if (i == 0 and j == 0) :
                MeanRelief[i][j] = (2 * DataElevation[i][j] - DataElevation[i][j + 1] - DataElevation[i + 1][j]) / 2
            elif (i == 0 and j == len(DataLon) - 1) :
                MeanRelief[i][j] = (2 * DataElevation[i][j] - DataElevation[i][j - 1] - DataElevation[i + 1][j]) / 2
            elif (i == len(DataLat) - 1 and j == 0) :
                MeanRelief[i][j] = (2 * DataElevation[i][j] - DataElevation[i][j + 1] - DataElevation[i - 1][j]) / 2
            elif (i == len(DataLat) - 1 and j == len(DataLon) - 1) :
                MeanRelief[i][j] = (2 * DataElevation[i][j] - DataElevation[i][j - 1] - DataElevation[i - 1][j]) / 2
            elif (i == 0) :
                MeanRelief[i][j] = (3 * DataElevation[i][j] - DataElevation[i][j - 1] - DataElevation[i][j + 1] - DataElevation[i + 1][j]) / 3
            elif (i == len(DataLat) - 1) :
                MeanRelief[i][j] = (3 * DataElevation[i][j] - DataElevation[i][j - 1] - DataElevation[i][j + 1] - DataElevation[i - 1][j]) / 3
            elif (j == 0) :
                MeanRelief[i][j] = (3 * DataElevation[i][j] - DataElevation[i + 1][j] - DataElevation[i - 1][j] - DataElevation[i][j + 1]) / 3
            elif (j == len(DataLon) - 1) :
                MeanRelief[i][j] = (3 * DataElevation[i][j] - DataElevation[i + 1][j] - DataElevation[i - 1][j] - DataElevation[i][j - 1]) / 3
            elif (i == 1 or i == len(DataLat) - 2 or j == 1 or j ==len(DataLon) - 2) :
                MeanRelief[i][j] = (4 * DataElevation[i][j] - DataElevation[i + 1][j] - DataElevation[i - 1][j] - DataElevation[i][j - 1] - DataElevation[i][j + 1]) / 3
            else :
                MeanRelief[i][j] = (4 * DataElevation[i][j] - DataElevation[i + 2][j] - DataElevation[i - 2][j] - DataElevation[i][j - 2] - DataElevation[i][j + 2]) / 4

    # 5) Barrier effect (in the circle of 0.2 degree)
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            if (i == 0 and j == 0) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i][j + 1], DataElevation[i][j] - DataElevation[i + 1][j])
            elif (i == 0 and j == len(DataLon) - 1) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i][j - 1], DataElevation[i][j] - DataElevation[i + 1][j])
            elif (i == len(DataLat) - 1 and j == 0) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i][j + 1], DataElevation[i][j] - DataElevation[i - 1][j])
            elif (i == len(DataLat) - 1 and j == len(DataLon) - 1) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i][j - 1], DataElevation[i][j] - DataElevation[i - 1][j])
            elif (i == 0) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i][j - 1], DataElevation[i][j] - DataElevation[i][j + 1], DataElevation[i][j] - DataElevation[i + 1][j])
            elif (i == len(DataLat) - 1) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i][j - 1], DataElevation[i][j] - DataElevation[i][j + 1], DataElevation[i][j] - DataElevation[i - 1][j])
            elif (j == 0) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i + 1][j], DataElevation[i][j] - DataElevation[i - 1][j], DataElevation[i][j] - DataElevation[i][j + 1])
            elif (j == len(DataLon) - 1) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i + 1][j], DataElevation[i][j] - DataElevation[i - 1][j], DataElevation[i][j] - DataElevation[i][j - 1])
            elif (i == 1 or i == len(DataLat) - 2 or j == 1 or j ==len(DataLon) - 2) :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i + 1][j], DataElevation[i][j] - DataElevation[i - 1][j], DataElevation[i][j] - DataElevation[i][j - 1], DataElevation[i][j] - DataElevation[i][j + 1])
            else :
                Barrier[i][j] = max(DataElevation[i][j] - DataElevation[i + 2][j], DataElevation[i][j] - DataElevation[i - 2][j], DataElevation[i][j] - DataElevation[i][j - 2], DataElevation[i][j] - DataElevation[i][j + 2])
    
    return TrendSurface1, TrendSurface2, MeanElevation, MeanRelief, Barrier

# Calculate multiple regression constants
def MultiRegress(type):
    
    # Calculate Spatial Distribution of Independent Variables
    # Variables: 1) First order surface; 2) second order surface; 3) mean elevation; 4) mean relief; 5) barrier effect.

    # Read in elevation data
    ed = Dataset('Spain02_v5.0_DD_010reg_orog.nc')
    
    DataElevation = ed.variables['orog'][:] # [latitude][longtitude]

    DataElevation = DataElevation.filled(0)

    # Read in alpha, kappa, threshold
    # Read in Station Paramter, alpha, kappa
    with open ('Station_Parameters.txt') as file_object :
        lines6 = file_object.readlines()
    dataset6 = [[] for i in range(len(lines6))]
    dataset06 = [[] for i in range(len(lines6))]
    for i in range(len(dataset06)):
        dataset06[i][:] = (item for item in lines6[i].strip().split(' '))
    
    # Delete invalid data caused by space
    for i in range(len(lines6)) :
        for j in range(len(dataset06[i])) :
            if dataset06[i][j] == '' :
                continue
            else :
                dataset6[i].append(dataset06[i][j])
    
    alpha = [0 for i in range(NoStation)]
    kappa = [0 for i in range(NoStation)]
    threshold = [0 for i in range(NoStation)]

    for i in range(NoStation) :
        if (dataset6[i + 1][1] == '0') :
            alpha[i] = 0
            kappa[i] = 0
            threshold[i] = 0
        else :
            alpha[i] = float(dataset6[i + 1][1])
            kappa[i] = float(dataset6[i + 1][2])
            threshold[i] = float(dataset6[i + 1][3])
    
    # Determine what parameters to fit
    y = [0 for i in range(NoStation)]

    if (type == 'alpha') :
        for i in range(NoStation) :
            y[i] = alpha[i]
    elif (type == 'kappa') :
        for i in range(NoStation) :
            y[i] = kappa[i]
    elif (type == 'threshold') :
        for i in range(NoStation) :
            y[i] = threshold[i]

    TrendSurface1 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    TrendSurface2 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanElevation = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanRelief = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    Barrier = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    TrendSurface1, TrendSurface2, MeanElevation, MeanRelief, Barrier = InVariableMap(DataElevation)

    # Calculate multiple regression constants with Matrix format
    n = 6
    x = [[0 for i in range(NoStation)] for j in range(n - 1)]

    for i in range(NoStation) :
        x[0][i] = TrendSurface1[MapLat[i]][MapLon[i]]
        x[1][i] = TrendSurface2[MapLat[i]][MapLon[i]]
        x[2][i] = MeanElevation[MapLat[i]][MapLon[i]]
        x[3][i] = MeanRelief[MapLat[i]][MapLon[i]]
        x[4][i] = Barrier[MapLat[i]][MapLon[i]]

    Xvariable = [[0 for i in range(n)] for j in range(n)]
    for i in range(n) :
        for j in range(n) :
            if (i == 0 and j == 0) :
                Xvariable[i][j] = NoStation
            elif (i == 0) : 
                Xvariable[i][j] = sum(x[j - 1][:])
            elif (j == 0) :
                Xvariable[i][j] = sum(x[i - 1][:])
            else :
                Xvariable[i][j] = prosum(x[i - 1][:],x[j - 1][:])
    Xvariable = np.array(Xvariable)

    Yvariable = [0 for i in range(n)]
    for i in range(n) :
        if (i == 0) :
            Yvariable[i] = sum(y[:])
        else :
            Yvariable[i] = prosum(x[i - 1][:], y[:])
    Yvariable = np.array(Yvariable)
    Yvariable = Yvariable.T

    b = np.dot(np.linalg.inv(Xvariable), Yvariable)
    print('The multiple regression constants of', type, 'is')
    print(b)

    return b

#b_alpha = MultiRegress('alpha')
#b_kappa = MultiRegress('kappa')
#b_threshold = MultiRegress('threshold')

# As calculated above
b_alpha = [1.71359597e+02, -6.52853331e-05, 6.52602785e-12, -3.28351062e-03, -4.59656238e-03, 7.55198727e-03]
b_kappa = [3.92923236e+00, -1.60312848e-06, 1.56112250e-13, 1.41953484e-04, 1.79773448e-04, -1.39290308e-04]
b_threshold = [1.31185109e+02, -4.91218603e-05, 4.96191172e-12, -2.58139589e-03, -2.60945962e-03, 8.20627152e-03]

# Spatial distribution
def SpatDistribution(type) :
    
    # Read in elevation data
    ed = Dataset('Spain02_v5.0_DD_010reg_orog.nc')
    
    DataElevation = ed.variables['orog'][:] # [latitude][longtitude]

    DataElevation = DataElevation.filled(0)

    n = 6
    # Determine what parameters to fit
    b = [0 for i in range(n)]

    if (type == 'alpha') :
        for i in range(n) :
            b[i] = b_alpha[i]
    elif (type == 'kappa') :
        for i in range(n) :
            b[i] = b_kappa[i]
    elif (type == 'threshold') :
        for i in range(n) :
            b[i] = b_threshold[i]

    # Create independent variables map
    TrendSurface1 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    TrendSurface2 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanElevation = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanRelief = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    Barrier = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    TrendSurface1, TrendSurface2, MeanElevation, MeanRelief, Barrier = InVariableMap(DataElevation)

    # Calculate parameters distribution
    parameter = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    parameterheat = [0 for i in range(len(DataLat) * len(DataLon))]
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            parameter[i][j] = b[0] + b[1] * TrendSurface1[i][j] + b[2] * TrendSurface2[i][j] + b[3] * MeanElevation[i][j] + b[4] * MeanRelief[i][j] + b[5] * Barrier[i][j]

    count = 0
    for i in range(len(DataLat)) :
        for j in range(len(DataLon)) :
            parameterheat[count] = parameter[i][j]
            count = count + 1

    # Plot heatmap of parameters
    # Construct location points
    ParameterDis = pd.DataFrame(
        {'Parameter': parameterheat,
         'Latitude': EP3857DataLat,
         'Longitude': EP3857DataLon})

    gParameterDis = ParameterDis.pivot_table(index='Latitude', 
                    columns = 'Longitude', 
                    values = 'Parameter', 
                    aggfunc = 'mean')
    ax = seaborn.heatmap(gParameterDis,
                        cmap = "YlGnBu", 
                        vmin = min(parameterheat),
                        vmax = max(parameterheat),
                        zorder = 1,
                        annot_kws = {'alpha':0.8}
                        )
    ax.invert_yaxis()

    # Add basemap to the plot
    ctx.add_basemap(ax, zoom=7)

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)

    plt.savefig('Spatial_Distribution_' + type + '_Heatmap.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
    plt.show()
    plt.close()

SpatDistribution('alpha')
SpatDistribution('kappa')
SpatDistribution('threshold')

#########################################################################################################################################################################################
# Predict Extreme Rainfall Events

# Return locations' distribution parameters
def ReParameter(ilat, ilon) :

    # Read in elevation data
    ed = Dataset('Spain02_v5.0_DD_010reg_orog.nc')
    
    DataElevation = ed.variables['orog'][:] # [latitude][longtitude]

    DataElevation = DataElevation.filled(0)

    n = 6
    # Determine what parameters to fit
    b = [[0 for i in range(n)] for j in range(3)]

    b[0][:] = b_alpha[:]
    b[1][:] = b_kappa[:]
    b[2][:] = b_threshold[:]

    # Create independent variables map
    TrendSurface1 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    TrendSurface2 = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanElevation = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    MeanRelief = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
    Barrier = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]

    TrendSurface1, TrendSurface2, MeanElevation, MeanRelief, Barrier = InVariableMap(DataElevation)

    ReParameter = [0 for i in range(3)]
    
    for k in range(3) :
        
        # Calculate parameters distribution
        parameter = [[0 for i in range(len(DataLon))] for j in range(len(DataLat))]
        for i in range(len(DataLat)) :
            for j in range(len(DataLon)) :
                 parameter[i][j] = b[k][0] + b[k][1] * TrendSurface1[i][j] + b[k][2] * TrendSurface2[i][j] + b[k][3] * MeanElevation[i][j] + b[k][4] * MeanRelief[i][j] + b[k][5] * Barrier[i][j]
        
        ReParameter[k] = parameter[ilat][ilon]

    return ReParameter[0], ReParameter[1], ReParameter[2]

# Return GP random variable with threshold given
def GP_rand(alpha, kappa, threshold) :
    
    U = random.uniform(0, 1)
    
    return alpha * (1 - (1 - U) ** kappa) / kappa + threshold

# Plot predicted/observed extreme rainfall events
def PredictEvents() :

    # Randomly select one coordinates
    ilat = random.randint(0, len(DataLat) - 1)
    ilon = random.randint(0, len(DataLon) - 1)

    # Read in the precipitation data of this place
    StaPr = [0 for i in range(len(DataTime))]
    for i in range(len(DataTime)) :
        StaPr[i] = DataPr[i][ilat][ilon]

    # Take extreme precipitaiton of largest 1200 values
    NoExtreme = 1200
    ExStaPr = [0 for i in range(NoExtreme)]

    ExStaPr[:] = NMaxElements(StaPr[:], NoExtreme)

    # Plot frequency map of observed extreme data
    ax1 = plt.subplot()
    ax1.hist(ExStaPr)
    plt.xlabel('Extreme Rainfall Events')
    plt.ylabel('Frequency')
    plt.title('Frequency Map of Observed Extreme Rainfall Events')
    plt.savefig('Extreme_Events_Frequency_Map_Observed.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
    plt.show()
    plt.close()

    # Plot frequency map of predicted extreme data
    alpha, kappa, threshold = ReParameter(ilat, ilon)
    
    PreEvents = [0 for i in range(NoExtreme)]

    for i in range(NoExtreme) :
        PreEvents[i] = GP_rand(alpha, kappa, threshold)
    
    PreEvents.sort()

    ax2 = plt.subplot()
    ax2.hist(PreEvents)
    plt.xlabel('Extreme Rainfall Events')
    plt.ylabel('Frequency')
    plt.title('Frequency Map of Predicted Extreme Rainfall Events')
    plt.savefig('Extreme_Events_Frequency_Map_Predicted.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
    plt.show()
    plt.close()

    # Plot probability plot of predicted/obserbed extreme data
    ax3 = plt.subplot()
    ax3.scatter(PreEvents, ExStaPr, linewidths = 3, color = 'blue', label = 'Predicted Extreme Values')
    ax3.plot(ExStaPr, ExStaPr, linewidth = 3, color = 'red', label = 'Expected Extreme Values')
    plt.legend()
    plt.xlabel('Predicted Extreme Rainfall Events')
    plt.ylabel('Observed Extreme Rainfall Events')
    plt.savefig('PP_Extreme_Events.png', dpi = 400, format = 'png', bbox_inches = 'tight', pad_inches=0)
    plt.show()
    plt.close()

#PredictEvents()