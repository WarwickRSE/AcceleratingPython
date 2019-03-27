import numpy as np
from timeit import default_timer as timer
import sys

def el_mult(A,B):
    n = A.shape[1]
    C = np.zeros([n,n])

    for i in range(0,n):
        for j in range(0,n):
            C[i,j] = A[i,j]*B[i,j] 
    return C

def gen_random_arrays(nels):
    start = timer()
    val = (np.random.rand(nels,nels), np.random.rand(nels,nels))
    end = timer()
    print("Generating random arrays takes ", end-start, " seconds")
    return val

def multiply_arrays(array_tuple):
    start = timer()
    val = el_mult(array_tuple[0], array_tuple[1])
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
