
import numpy as np
from sys import argv
import time

# This lets us turn on or off jit (jjust-in time compilation)
# using a single variable rather than having to adjust inside the code
use_jit = True
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

def main(num_items, num_high, iterations):

  #Run multiple iterations and find the average time
  array = create_two_valued_array(num_items, num_high)

  #Ensure jit-ter has run
  any = exceeds(array, 5)
  #Ensure jit-ter has run
  any = early_terminating_exceeds(array, 5)

  min_time = 1e5
  max_time = 0.0
  cum_time = 0.0
  for i in range(iterations):
    array = create_two_valued_array(num_items, num_high)

    start_time = time.time()
    any = exceeds(array, 5)
    end_time = time.time()
    cum_time += (end_time - start_time)
    min_time = min(min_time, (end_time-start_time))
    max_time = max(max_time, (end_time-start_time))

  min_time_b = 1e5
  max_time_b = 0.0
  cum_time_b = 0.0
  for i in range(iterations):
    array = create_two_valued_array(num_items, num_high)

    start_time = time.time()
    any = early_terminating_exceeds(array, 5)
    end_time = time.time()
    cum_time_b += (end_time - start_time)
    min_time_b = min(min_time_b, (end_time-start_time))
    max_time_b = max(max_time_b, (end_time-start_time))

  print("Full loop took (average, min, max)       {:.3e} s, {:.3e} s, {:.3e} s".format(cum_time/iterations, min_time, max_time))
  print("Early-term loop took (average, min, max) {:.3e} s, {:.3e} s, {:.3e} s".format( cum_time_b/iterations, min_time_b, max_time_b))


if __name__ == "__main__":

  try:
    num_items = int(argv[1])
    num_high = int(argv[2])
  except:
    num_items = 100000
    num_high = 1
  try:
    num_iter = int(argv[3])
  except:
    num_iter = 100

  print("Using ", num_items, num_high)
  print("For ", num_iter, " iterations")
  main( num_items, num_high, num_iter)
