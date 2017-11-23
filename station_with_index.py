#!/opt/anaconda3/bin/python3.5m

import csv
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


def writeToFile(input, output):
    fileIR = 'data/irdata/ir08nc/IR08_20170601_0000.nc'
    fileIR = Dataset(fileIR, 'r')

    var = fileIR.variables
    lat = var['latitude'][:]
    long = var['longitude'][:]

    with open(output, 'w') as file:
        with open(input, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            w = []
            i = 0
            station = 0
            for row in reader:
                w.append(row[1])
                if(i != 0):
                    if(w[i-1] != w[i]):
                        station += 1
                        lat_idx = find_index(float(row[1]), lat)
                        long_idx = find_index(float(row[2]), long)

                        if isinstance(lat_idx, list):
                            lat_idx = ';'.join(map(str, lat_idx))
                            long_idx = ';'.join(map(str, long_idx))
                        else:
                            lat_idx = str(lat_idx)
                            long_idx = str(long_idx)

                        file.write(str(station) + ',' + row[1] + ',' + row[2] + ',' + lat_idx + ',' + long_idx + '\n')
                else:
                    lat_idx = find_index(float(row[1]), lat)
                    long_idx = find_index(float(row[2]), long)

                    if isinstance(lat_idx, list):
                        lat_idx = ';'.join(map(str, lat_idx))
                        long_idx = ';'.join(map(str, long_idx))
                    else:
                        lat_idx = str(lat_idx)
                        long_idx = str(long_idx)

                    file.write(str(station) + ',' + row[1] + ',' + row[2] + ',' + lat_idx + ',' + long_idx + '\n')
                i += 1

def main():
    input = 'data/rain/5-9_2017.csv'
    output = 'sample_data/rain/station_with_index2.csv'

    writeToFile(input, output)

if __name__ == "__main__":
    main()
