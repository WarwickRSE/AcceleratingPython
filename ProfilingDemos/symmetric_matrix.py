
import numpy as np
import math
import time
from sys import argv

#Pick exactly one of this pair:
#----------------------------------
try:
  b = int(argv[1])
except:
  b = 0

#Use jit on core
if b == 1:
  print("Jitting core function")
  from numba import jit
else:
#Or don't
  print("No jitting")
  def jit(fn):
    def wrapper(*args):
      return fn(*args)
    return wrapper
#----------------------------------



@jit
def calc(num):

  return math.exp(num)

#Force jit on import
a=calc(1)

calcv = np.vectorize(calc)

@jit
def calc1(num):

  return num+1

#Force jit on import
a=calc1(1)

calc1v = np.vectorize(calc1)

def applyToSymmetricMatrix(matrix, func):

  start = time.time()
  indices = np.triu_indices(np.size(matrix, axis=0))
  end = time.time()
  print("         Generating indices took ", end-start, ' s')
  matrix[indices] = func(matrix[indices])

  forceEval(matrix)
  return matrix

def applyToSquareSymmetricMatrix(matrix, func):

  indices = np.shape(matrix)
  for i in range(0,indices[0]):
    for j in range(i, indices[1]):
      matrix[i, j] = func(matrix[i, j])

  forceEval(matrix)
  return matrix

def applyFuncLoop(matrix, func):

  indices = np.shape(matrix)
  for i in range(0,indices[0]):
    for j in range(0,indices[1]):
      matrix[i, j] = func(matrix[i, j])

  forceEval(matrix)
  return matrix

def applyFuncForIn(matrix, func):

  for element in matrix:
    element = func(element)

  forceEval(matrix)
  return matrix

def applyFunc(matrix, func):

  matrix = func(matrix)
  forceEval(matrix)
  return matrix

def forceEval(matrix):
  print(np.sum(matrix))

def main():

  func = calc1
  funcv = calc1v
  sz = 500
  matrix = np.ones((sz, sz))

  start = time.time()
  applyFunc(matrix, funcv)
  end = time.time()

  print("Call took          ", end-start, " s")

  start = time.time()
  applyFuncForIn(matrix, func)
  end = time.time()

  print("For-in loop took   ", end-start, " s")

  start = time.time()
  applyFuncLoop(matrix, func)
  end = time.time()

  print("Simple loop took   ", end-start, " s")

  start = time.time()
  applyToSquareSymmetricMatrix(matrix, func)
  end = time.time()

  print("Square method took ", end-start, " s")

  start = time.time()
  applyToSymmetricMatrix(matrix, funcv)
  end = time.time()

  print("Clever method took ", end-start, " s")

if __name__ == "__main__":

  main()


