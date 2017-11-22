#!/opt/anaconda3/bin/python3.5m

import os
import glob
import sys
import json
import time
import csv
import numpy as np
from netCDF4 import Dataset

def avg_value(x, lat, long):
    total = 0
    for i in lat:
        for j in long:
            total += x[int(i)][int(j)]
    val = total / (len(lat) * len(long))
    return val

def get_station_index(path):
    station = []
    with open(path, 'r') as file:
        data = csv.reader(file, delimiter=',')
        for row in data:
            station.append([row[1], row[2], row[3], row[4]])
    return station

def get_ncname(ir, ir_loc, file):
    if(ir == 'IR08'):
        nc_file = ir_loc[0] + file
    if(ir == 'IR13'):
        nc_file = ir_loc[1] + file
    if(ir == 'IR15'):
        nc_file = ir_loc[2] + file
    return nc_file

def get_attribute(filename):
    ir = filename[0]
    date = filename[1]
    time = filename[2]
    hour = time[0] + time[1]
    minute = time[2] + time[3]
    return ir, date, time, hour, minute

def create_data(file, station, ir_loc):
    dataIR = ['IR08', 'IR13', 'IR15']
    nc_file = ''
    data = {}
    for ir in dataIR:
        nc_file = get_ncname(ir, ir_loc, file)
        for filename in glob.iglob(nc_file):
            if('\\' in filename):
                filename = filename.replace('\\', '/')
            fileIR = filename

            filename = filename.split('/')[-1].replace('.nc', '')
            filename = filename.split('_')
            ir, date, time, hour, minute = get_attribute(filename)
            
            for i in range(0, len(station)):
                latlong = str(station[i][0]) + ';' + str(station[i][1])
                lat_idx = station[i][2]
                long_idx = station[i][3]
                if ir in data:
                    if date in data[ir]:
                        if hour in data[ir][date]:
                            if minute in data[ir][date][hour]:
                                data[ir][date][hour][minute][latlong] = cal_val(lat_idx, long_idx, fileIR, ir)
                            else:
                                data[ir][date][hour][minute] = {}
                                data[ir][date][hour][minute][latlong] = cal_val(lat_idx, long_idx, fileIR, ir)
                        else:
                            data[ir][date][hour] = {}
                            data[ir][date][hour][minute] = {}
                            data[ir][date][hour][minute][latlong] = cal_val(lat_idx, long_idx, fileIR, ir)
                    else:
                        data[ir][date] = {}
                        data[ir][date][hour] = {}
                        data[ir][date][hour][minute] = {}
                        data[ir][date][hour][minute][latlong] = cal_val(lat_idx, long_idx, fileIR, ir)
                else:
                    data[ir] = {}
                    data[ir][date] = {}
                    data[ir][date][hour] = {}
                    data[ir][date][hour][minute] = {}
                    data[ir][date][hour][minute][latlong] = cal_val(lat_idx, long_idx, fileIR, ir)

            #fileIR.close()
    return data

def cal_val(lat, long, fileIR, ir):
    if(';' in lat):
        lat_idx = lat.split(';')
        long_idx = long.split(';')
    else:
        lat_idx = lat
        long_idx = long
    fileIR = Dataset(fileIR, 'r')
    val = 0
    var = fileIR.variables
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

    if(isinstance(lat_idx, list)):
        val = str(avg_value(tbb, lat_idx, long_idx))
        print(type(val))
    else:
        val = str(tbb[int(lat_idx)][int(long_idx)])
    #if(val == '--'):
    #    print('eiei')
    #    val = -1
    fileIR.close()
    return val

def writeToJson(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def main():
    fileIR_date = '_20170601_00*'
    root = 'data'

    output = 'dataset/input/dataset.json'
    ir_root = root + '/irdata/'

    station = get_station_index(root + '/rain/station_with_index2.csv')
    ir_loc = [ir_root + 'ir08nc/IR08', ir_root + 'ir13nc/IR13', ir_root + 'ir15nc/IR15']

    start_time = time.time()
    data = create_data(fileIR_date, station, ir_loc)
    print("--- %s seconds ---" % (time.time() - start_time))

    writeToJson(data, output)

if __name__ == "__main__":
    main()