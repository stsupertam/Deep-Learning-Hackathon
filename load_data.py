#!/opt/anaconda3/bin/python3.5m

import h5py

with h5py.File('dataset/data_2.h5', 'r') as hf:
    X = hf['input'][:]
    y = hf['output'][:]
    z = hf['attribute'][:]

print(X.shape)
print(y.shape)
print(z[0])