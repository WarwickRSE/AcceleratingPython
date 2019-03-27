
try:
    from ctypes import *
except:
    print("Cannot import ctypes")
    raise

from math import sqrt, trunc
import numpy
from time import time

check_prime = None
primes_in_range = None

def load_so():
    global primes_in_range, check_prime

    so = CDLL('./c_library/functions_O.so')
    so.primes_in_range.argtypes=[c_long, c_long]
    so.primes_in_range.restype =c_long
    primes_in_range = so.primes_in_range

    so.check_prime.argtypes=[c_long]
    so.check_prime.restype =c_byte
    check_prime = so.check_prime

print("Using C functions")
start = time()
#Import shared obj
a=load_so()
end = time()
print("Imported in ", end-start, "s")

start = time()
#Call check_prime to make sure imports worked
print("Testing 32452843 is ", check_prime(32452843))
end = time()
print("Test call ran in ", end-start, "s")
