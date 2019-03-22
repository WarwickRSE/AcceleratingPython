import numpy as np
import pickle
import shelve
import zlib
import gzip
from timeit import default_timer
def output(data):

    #Write binary file without any metadata
    #This isn't a good idea really
    start = default_timer()
    fh=open('out.dat','wb')
    for i in data:
        fh.write(bytearray(i))
    fh.close()
    end = default_timer()
    print('Data written OK in {} seconds'.format(end-start))

def output_compress(data):

    #Write binary file without any metadata and with compression
    #This isn't a good idea really
    start = default_timer()
    fh=gzip.open('out_compress.gz','wb')
    for i in data:
        fh.write(bytearray(i))
    fh.close()
    end = default_timer()
    print('Data written OK in {} seconds'.format(end-start))

def output_pickle(data):

    #Write binary file in pickle format
    #This is better but is painfully slow in Python2
    #And there are few guarantees about pickle formats
    start = default_timer()
    fh=open('out_pickle.dat','wb')
    fh.write(pickle.dumps(data))
    fh.close()
    end = default_timer()
    print('Data written OK in {} seconds'.format(end-start))

def output_pickle_compress(data):

    #Write binary file in pickle format
    #This is better but is painfully slow in Python2
    #And there are few guarantees about pickle formats
    start = default_timer()
    fh=gzip.open('out_pickle.dat','wb')
    fh.write(pickle.dumps(data))
    fh.close()
    end = default_timer()
    print('Data written OK in {} seconds'.format(end-start))

def output_shelve(data):
    start = default_timer()
    out = shelve.open('out_shelve.dat')
    for num, val in enumerate(data):
        out[str(num)] = val
    out.close()
    end = default_timer()
    print('Data written OK in {} seconds'.format(end-start))


def gen_random_data(n_els=100):
    return[np.random.rand(1000,1000) for el in range(n_els)]

def gen_uniform_data(n_els=100):
    return [np.ones([1000,1000]) for el in range(n_els)]

def gen_sine_data(n_els=100):
    x = np.linspace(0, 2.0*np.pi, 1000)
    y = np.linspace(0, 2.0*np.pi, 1000)
    xv, yv = np.meshgrid(x, y)
    return [np.sin(xv*yv) for el in range(n_els)]
    
