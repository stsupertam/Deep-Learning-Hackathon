#!/opt/anaconda3/bin/python3.5m

import json
import numpy as np
import time
import h5py
import csv
import glob

def load_data(inp, out):
    output_data = []
    with open(inp, 'r') as file:
        input_data = json.load(file)
    with open(out, 'r') as file:
        output = csv.reader(file, delimiter=',')
        for row in output:
            output_data.append(row)
    return input_data, output_data

def get_time(timestamp):
    date = timestamp[0].replace('-', '')
    hour = timestamp[1].split(':')[0]
    minute = timestamp[1].split(':')[1]
    return date, hour, minute

def map_inout(input_data, output_data):
    X = []
    y = []
    z = []
    ir = ['IR08', 'IR13', 'IR15']
    for row in output_data:
        if(str(row[-1]) != '-1'):
            latlong = row[1] + ';' + row[2]
            timestamp = row[0].split(' ')
            date, hour, minute = get_time(timestamp)
            temp = []
            restart = False
            for item in ir:
                temp2 = []
                if(item in input_data):
                    if(date in input_data[item]):
                        if(hour in input_data[item][date]):
                            j = 0
                            for i in input_data[item][date][hour]:
                                j += 1
                                if(latlong in input_data[item][date][hour][i]):
                                    if(input_data[item][date][hour][i][latlong] != '--'):
                                        temp2.append(float(input_data[item][date][hour][i][latlong]))
                                else:
                                    restart = True
                            if(len(temp2) < 6):
                               total = sum(map(float, temp2))
                               missing = 6 - len(temp2)
                               avg = total / len(temp2)
                               for i in range(0, missing):
                                   temp2.append(avg)
                        else:
                            restart = True
                    else:
                        restart = True
                else:
                    restart = True
                temp.extend(temp2)
            if(not restart):
                X.append(temp)
                y.append(float(row[-1]))
                z.append(row[:-1])
            else:
                restart = False
    return X, y, z

def writeToFile(X, y, z, output):
    X = np.array(X)
    y = np.array(y)
    z = np.array(z)
    with h5py.File(output, 'w') as hf:
        hf.create_dataset('input', data=X)
        hf.create_dataset('output', data=y)
        hf.create_dataset('attribute', data=z)

def main():
    root = 'dataset'
    input_json = root + '/input/dataset06*'
    output_csv = root + '/output/5-9_2017_edit_none.csv'

    X = []
    y = []
    z = []
    outputfile = root + '/data_2.h5'

    start_time = time.time()
    for input in glob.iglob(input_json):
        input_data, output_data = load_data(input, output_csv)
        a, b, c = map_inout(input_data, output_data)
        X.extend(a)
        y.extend(b)
        z.extend(c)

    #writeToFile(X, y, z, outputfile)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()

