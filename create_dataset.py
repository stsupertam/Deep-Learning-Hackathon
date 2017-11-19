import os
import glob
import sys
import csv
import numpy as np
import h5py
from netCDF4 import Dataset, num2date

def find_index(xvar, x, avg=None):
    indx = None
    list_indx = []
    if x[0] > x[-1]:
        for i in range(len(x)):
            if x[i] < xvar:
                indx = i
                if(avg != None):
                    if(i == 1):
                        list_indx.extend([i-1, i])
                    else:
                        list_indx.extend([i-1, i, i+1])
                    return list_indx
                if abs(x[i - 1] - xvar) < abs(x[i] - xvar):
                        indx = i - 1
                break
    else:
        for i in range(len(x)):
            if x[i] > xvar:
                indx = i
                if(avg != None):
                    if(i == 1):
                        list_indx.extend([i-1, i])
                    else:
                        list_indx.extend([i-1, i, i+1])
                    return list_indx
                if abs(x[i - 1] - xvar) < abs(x[i] - xvar):
                        indx = i - 1
                break
    return indx

def avg_value(x, lat, long):
    total = 0
    for i in lat:
        for j in long:
            print(x[i][j])
            total += x[i][j]
    val = total / (len(lat) * len(long))
    return val

def eiei():
    reset()
def writeToFile():
    pass
def main():
    select = '201709*.nc'
    fileIR08 = 'data/irdata/ir08nc/IR08_' + select
    fileIR13 = 'data/irdata/ir13nc/IR13_' + select
    fileIR15 = 'data/irdata/ir15nc/IR15_' + select
    writeToFile()
    output = open('data/rain/5-9_2017.csv', 'r')

    slat = 24.8741
    slong = 95.0
    var = file.variables
    dim = file.dimensions
    tbb08 = var['tbb13']
    tbb13 = var['tbb13']
    tbb15 = var['tbb13']
    list_lat = var['latitude'][:]
    list_long = var['longitude'][:]

    lat_idx = find_index(slat, list_lat, 'a')
    long_idx = find_index(slong, list_long, 'a')

    if isinstance(lat_idx, list):
        tbb08 = avg_value(tbb08, lat_idx, long_idx)
        tbb13 = avg_value(tbb13, lat_idx, long_idx)
        tbb15 = avg_value(tbb15, lat_idx, long_idx)

    fileIR08.close()
    fileIR13.close()
    fileIR15.close()
    output.close()


if __name__ == "__main__":
    main()

