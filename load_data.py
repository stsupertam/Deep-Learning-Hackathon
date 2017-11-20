import h5py

with h5py.File('sample_data/data.h5', 'r') as hf:
    X = hf['input'][:]
    y = hf['output'][:]

print(X)
print(y)