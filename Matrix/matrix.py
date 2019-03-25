import numpy as np
from timeit import default_timer as timer
import sys

def gen_random_matrices(nels):
    start = timer()
    val = (np.random.rand(nels,nels), np.random.rand(nels,nels))
    end = timer()
    print("Generating random matrices takes ", end-start, " seconds")
    return val

def multiply_matrices(mat_tuple):
    start = timer()
    val = mat_tuple[0].dot(mat_tuple[1])
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
    nels = 10000

  print("Multiplying ", nels, " square matrices together")
  main(nels)
