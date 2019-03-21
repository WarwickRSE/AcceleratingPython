
try:
    from ctypes import *
except:
    print("Cannot import ctypes")
    raise

from math import sqrt, trunc
import numpy
from time import time

check_prime = None

#def check_prime(num):
#  global check_prime_int
#  return check_prime_int(num)

def load_so():
    global check_prime

    so = CDLL('./c_call_example/functions_O.so')
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
