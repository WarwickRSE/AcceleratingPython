
try:
  from numba import jit
except:
  print("Cannot import numba for jit")
  raise

from math import sqrt, trunc
import numpy
from time import time


@jit
def check_prime(num):

  has_divisor = False

  #Check 2 specially
  if num%2 == 0:
    return False
  #Ignore all other as 2 was false
  for i in range(3, trunc(sqrt(num))+1, 2):
    if num%i == 0:
      has_divisor = True
      break
  return not has_divisor

print("Using jitted functions")
start = time()
#Call check_prime to make sure jit runs now
a=check_prime(2)
end = time()
print("Compiled 1 function in ", end-start, "s")
