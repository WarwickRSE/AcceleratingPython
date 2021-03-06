import numpy as np
from timeit import default_timer as timer
import sys
from numba import jit, njit

@njit
def dot_py(A,B,C):
    n = A.shape[1]

    for i in range(0,n):
        for j in range(0,n):
            for k in range(0,n):
                C[i,j] += A[i,k]*B[k,j] 
    return C

def gen_random_matrices(nels):
    start = timer()
    val = (np.random.rand(nels,nels), np.random.rand(nels,nels))
    end = timer()
    print("Generating random matrices takes ", end-start, " seconds")
    return val

def multiply_matrices(mat_tuple):
    start = timer()
    n = mat_tuple[0].shape[1]
    C = np.zeros([n,n])
    val = dot_py(mat_tuple[0], mat_tuple[1],C)
    end = timer()
    print("Multiplying random matrices takes ", end-start, " seconds")
    return val

def main(nels):
    dat = gen_random_matrices(nels)
    result = multiply_matrices(dat)


if __name__ == "__main__":

  try:
    nels = int(sys.argv[1])
  except:
    nels = 200

  print("Multiplying ", nels, " square matrices together")
  main(nels)
