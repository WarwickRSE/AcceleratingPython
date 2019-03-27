
import numpy as np
from sys import argv
import time

# This lets us turn on or off jit (just-in time compilation)
# using a single variable rather than having to adjust inside the code
use_jit = False
if use_jit == True:
  #Use jit on core
  print("Jitting core function")
  from numba import jit
else:
  #Or don't
  print("No jitting")
  #Create dummy function instead
  def jit(fn):
    def wrapper(*args):
      return fn(*args)
    return wrapper
#----------------------------------

def create_two_valued_array(n_items, n_high):

  array1 = np.ones(n_items-n_high)
  array2 = np.ones(n_high)*10

  return np.random.permutation(np.concatenate((array1, array2)))

@jit
def exceeds(array, exceeds_val):

  result = False
  for el in array:
    if el > exceeds_val: result = True

  return result

@jit
def early_terminating_exceeds(array, exceeds_val):

  for el in array:
    if el > exceeds_val: return True

  return False

@jit
def compiled_in(array, in_val):
  return in_val in array

def main(num_items, num_high):

  array = create_two_valued_array(num_items, num_high)

  start_time = time.time()
  max = np.max(array)
  end_time = time.time()
  print("Found max in ", end_time-start_time, "s")

  start_time = time.time()
  any = np.any(array >= 10)
  end_time = time.time()
  print("Found any in ", end_time-start_time, "s")

  start_time = time.time()
  any = (10 in array)
  end_time = time.time()
  print("Found 'in' in ", end_time-start_time, "s")

  #Run compile before we time it
  any = compiled_in(array, 10)
  start_time = time.time()
  any = compiled_in(array, 10)
  end_time = time.time()
  print("Found 'in' w. compilation in ", end_time-start_time, "s")


  #Ensure jit-ter has run
  any = exceeds(array, 5)

  start_time = time.time()
  any = exceeds(array, 5)
  end_time = time.time()
  print("Found first exceeds in ", end_time-start_time, "s")

  #Ensure jit-ter has run
  any = early_terminating_exceeds(array, 5)

  start_time = time.time()
  any = early_terminating_exceeds(array, 5)
  end_time = time.time()
  print("Found first exceeds (w term) in ", end_time-start_time, "s")


if __name__ == "__main__":

  try:
    num_items = int(argv[1])
    num_high = int(argv[2])
  except:
    num_items = 10000
    num_high = 10

  print("Using ", num_items, num_high)
  main( num_items, num_high)
