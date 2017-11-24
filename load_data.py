#!/opt/anaconda3/bin/python3.5m

import h5py

with h5py.File('dataset/data_6.h5', 'r') as hf:
    X = hf['input'][:]
    y = hf['output'][:]

for i in range(0, X.shape[0]):
    if(-1 in X[i]):
        print('Bug Bug')
    elif('-1' in X[i]):
        print('Fucking Bug')