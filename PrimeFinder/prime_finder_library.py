from sys import argv
from numpy import zeros, sum

from c_library.functions import check_prime, primes_in_range

import time


@jit
def main_loop(lower, length, flags):
  for i in range(1, length):
    flags[i] = check_prime(lower+i)

def main_serial(lower, upper):

  length = upper - lower
  flags = zeros(length)
  start_time = time.time()
  main_loop(lower, length, flags)
  end_time = time.time()
  print("Found ", int(sum(flags)), " primes in", end_time-start_time, ' s using C core function')

  length = upper - lower
  flags = zeros(length)
  start_time = time.time()
  primes = primes_in_range(lower, upper)
  end_time = time.time()
  print("Found ", primes, " primes in", end_time-start_time, ' s using C for everything')


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

