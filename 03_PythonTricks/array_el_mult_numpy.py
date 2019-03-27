import numpy as np
from timeit import default_timer as timer
import sys

def gen_random_arrays(nels):
    start = timer()
    val = (np.random.rand(nels,nels), np.random.rand(nels,nels))
    end = timer()
    print("Generating random arrays takes ", end-start, " seconds")
    return val

def multiply_arrays(array_tuple):
    start = timer()
    val = array_tuple[0] * array_tuple[1]
    end = timer()
    print("Multiplying random arrays elementwise takes ", end-start, " seconds")
    return val

def main(nels):
    dat = gen_random_arrays(nels)
    result = multiply_arrays(dat)

if __name__ == "__main__":

  try:
    nels = int(sys.argv[1])
  except:
    nels = 2000

  print("Multiplying ", nels, " square arrays together elementwise")
  main(nels)
