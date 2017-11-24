#!/opt/anaconda3/bin/python3.5m

import h5py

with h5py.File('dataset/data_5.h5', 'r') as hf:
    X = hf['input'][:]
    y = hf['output'][:]

print(X.shape)
print(y.shape)