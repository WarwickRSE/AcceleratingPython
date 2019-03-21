from sys import argv
from numpy import zeros, sum

#Pick exactly one of this pair:
#----------------------------------
b = 1
#Use jit on main loop
if b == 1:
  print("Jitting main loop")
  from numba import jit
else:
#Or don't
  print("Pure main loop")
  def jit(fn):
    def wrapper(a, b):
      fn(a, b)
    return wrapper
#----------------------------------

#Pick ONE of the following to
#demonstrate various speedups
try:
  a = int(argv[1])
except:
  a = 2

if a == 0:
  #Base
  from base_example.functions import check_prime
elif a == 1:
  #jitting heavy functions
  from jit_example.functions import check_prime
elif a == 2:
  #Off loading heavy functions to C
  from c_call_example.functions import check_prime

import time

primes = []

@jit
def main_serial(lower, upper):

  length = upper - lower
  flags = zeros(length)
  #Offset of last dispatched value
  start_time = time.time()
  for i in range(1, length):
    flags[i] = check_prime(lower+i)
  end_time = time.time()
  print("Found ", int(sum(flags)), " primes in", end_time-start_time, ' s')


if __name__ == "__main__":

  try:
    lower = int(input('Enter lower bnd: '))
  except:
    print("I didn't understand. I'll try 100000")
    lower = 100000
  try:
    upper = int(input('Enter upper bnd: '))
  except:
    print("I didn't understand. I'll try 200000")
    upper = 200000

  main_serial(lower, upper)

