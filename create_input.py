import os
import glob
import sys
import json
import time
import csv
import numpy as np
from netCDF4 import Dataset

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
            total += x[i][j]
    val = total / (len(lat) * len(long))
    return val

def get_station_latlong(path):
    station = []
    with open(path, 'r') as file:
        data = csv.reader(file, delimiter=',')
        for row in data:
            station.append([row[1], row[2]])
    return station

def create_data(file, station, ir_loc):
    dataIR = ['IR08', 'IR13', 'IR15']
    nc_file = ''
    data = {}
    for ir in dataIR:
        if(ir == 'IR08'):
            nc_file = ir_loc[0] + file
        if(ir == 'IR13'):
            nc_file = ir_loc[1] + file
        if(ir == 'IR15'):
            nc_file = ir_loc[2] + file
        for filename in glob.iglob(nc_file):
            if('\\' in filename):
                filename = filename.replace('\\', '/')
            fileIR = filename

            filename = filename.split('/')[-1].replace('.nc', '')
            filename = filename.split('_')
            ir = filename[0]
            date = filename[1]
            time = filename[2]

            hour = time[0] + time[1]
            minute = time[2] + time[3]
            #print(date)
            
            for i in range(0, len(station)):
                latlong = str(station[i][0]) + ';' + str(station[i][1])
                if ir in data:
                    if date in data[ir]:
                        if hour in data[ir][date]:
                            if minute in data[ir][date][hour]:
                                data[ir][date][hour][minute][latlong] = cal_val(latlong, fileIR, ir)
                            else:
                                data[ir][date][hour][minute] = {}
                                data[ir][date][hour][minute][latlong] = cal_val(latlong, fileIR, ir)
                        else:
                            data[ir][date][hour] = {}
                    else:
                        data[ir][date] = {}
                        data[ir][date][hour] = {}
                        data[ir][date][hour][minute] = {}
                        data[ir][date][hour][minute][latlong] = cal_val(latlong, fileIR, ir)
                else:
                    data[ir] = {}
                    data[ir][date] = {}
                    data[ir][date][hour] = {}
                    data[ir][date][hour][minute] = {}
                    data[ir][date][hour][minute][latlong] = cal_val(latlong, fileIR, ir)

            #fileIR.close()
    return data

def cal_val(latlong, fileIR, ir):
    latlong = latlong.split(';')
    slat = latlong[0]
    slong = latlong[1]
    fileIR = Dataset(fileIR, 'r')
    var = fileIR.variables
    val = 0
    if(ir == 'IR08'):
        if('tbb08' in var):
            tbb = var['tbb08']
        else:
            return -1
    if(ir == 'IR13'):
        if('tbb13' in var):
            tbb = var['tbb13']
        else:
            return -1
    if(ir == 'IR15'):
        if('tbb15' in var):
            tbb = var['tbb15']
        else:
            return -1
    
    list_lat = var['latitude'][:]
    list_long = var['longitude'][:]

    lat_idx = find_index(float(slat), list_lat, 'a')
    long_idx = find_index(float(slong), list_long, 'a')

    if isinstance(lat_idx, list):
        val = avg_value(tbb, lat_idx, long_idx)
    else:
        val = tbb[lat_idx][long_idx]
    return val

def writeToJson(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def main():
    fileIR_date = '_201706*'
    root = 'sample_data'

    output = 'dataset/input/dataset.json'
    ir_root = root + '/irdata/'

    station = get_station_latlong(root + '/rain/station.csv')
    ir_loc = [ir_root + 'ir08nc/IR08', ir_root + 'ir13nc/IR13', ir_root + 'ir15nc/IR15']

    start_time = time.time()
    data = create_data(fileIR_date, station, ir_loc)
    print("--- %s seconds ---" % (time.time() - start_time))

    writeToJson(data, output)

if __name__ == "__main__":
    main()