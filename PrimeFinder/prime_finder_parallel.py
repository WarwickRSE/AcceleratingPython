from sys import argv
from numba import jit

try:
  from mpi4py import MPI as MPI
  has_mpi = True
except:
  has_mpi = False

#Off loading heavy functions to C
from c_call_example.functions import *

import time

primes = []

#Block up the work a bit
#Default to ten
nblocks = 10

def controller(lower, upper):

  global nblocks
  #Set up the basic MPI stuff
  comm = MPI.COMM_WORLD
  nproc = comm.Get_size()
  rank = comm.Get_rank()

  #Setup values for array of flags
  length = upper - lower
  flags = numpy.zeros(length)
  #Offset of last dispatched value
  current_val = 0

  #Number of in-flight work packets
  inflight = 0

  #Arrays holding data per worker:
  #Value last sent to worker
  vals_in_use = numpy.zeros((nproc-1, nblocks))

  #Workers stats - how many processed in how long
  processed = numpy.zeros(nproc-1)
  start_time = numpy.zeros(nproc-1)
  cum_time = numpy.zeros(nproc-1)
  end_time = numpy.zeros(nproc-1)

  #Some things need to have the correct type BEFORE the MPI calls
  info = MPI.Status()

  while True:
    #Wait for message from workers
    # On first pass we expect to get info.tag of zero signalling "ready"
    # After that we get a non-zero tag signalling "done"
    results = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=info)

    if info.tag > 0:
      # Capture stats
      end_time[info.source-1] = time.time()
      cum_time[info.source-1] = cum_time[info.source-1] + (end_time[info.source-1] - start_time[info.source-1])
      processed[info.source-1] = processed[info.source-1] + 1
      #Store result
      #Result is True (1) if prime, False (0) else

      offset = vals_in_use[info.source-1, 0] - lower

      #Last block might include values outside target range
      if(offset+nblocks <= length):
        flags[int(offset):int(offset)+nblocks] = results
      else:
        flags[int(offset):length] = results[0:length-int(offset)-nblocks]
      inflight = inflight - 1

    if current_val < length:
      #If there is still work to do, reply with next package
      for i in range(0,nblocks):
        vals_in_use[info.source-1, i] = lower + current_val + i
      #print("Dispatching ", lower+current_val)

      start_time[info.source-1] = time.time()
      current_val = current_val + nblocks
      comm.send(vals_in_use[info.source-1,:], dest=info.source, tag=1)
      inflight = inflight + 1
    else:
      #No more work, shut down the worker
      comm.send(1, dest=info.source, tag=0)

    if inflight == 0:
      #Nothing is in flight, all done
      break

  #Summarize findings
  for i in range(0, nproc-1):
    print("Worker ", i, " processed ", int(processed[i-1]), " packets in ", cum_time[i-1], "s")
  print("Packet length ", nblocks)

  print("Found ", int(numpy.sum(flags)), " primes")

def worker():
  global nblocks

  comm = MPI.COMM_WORLD

  #Send initial message with dummy data and tag =0 for "ready"
  results = [0]*nblocks
  comm.send(results, dest=0, tag=0)

  while True:
    #Wait for a message
    tag = 0
    info = MPI.Status()
    candidates = comm.recv(source=0, tag=MPI.ANY_TAG, status=info)
    tag = info.tag
    if(tag > 0):
      #Got number to check, check and return
      for i in range(0,nblocks):
        cand = int(candidates[i])
        results[i] = check_prime(int(candidates[i]))
      comm.send(results, dest=0, tag=tag)
    else:
      #Shutdown - nothing more to do
      return

@jit
def main_parallel(lower, upper):
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  if rank == 0:
    controller(lower, upper)
  else:
    worker()

@jit
def main_serial(lower, upper):

  length = upper - lower
  flags = numpy.zeros(length)
  #Offset of last dispatched value
  start_time = time.time()
  for i in range(1, length):
    flags[i] = check_prime(lower+i)
  end_time = time.time()

  print("Found ", int(numpy.sum(flags)), " primes in", end_time-start_time, ' s')


if __name__ == "__main__":

  if has_mpi:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nproc = comm.Get_size()

     #Take two values describing range to check, [lower, upper]
    if(rank ==0):
      #Notify that multicore is available
      if(nproc == 1): print("Found mpi4py, can run on multiple cores")
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
    else:
      lower = 0
      upper = 0

    if nproc > 1:
      main_parallel(lower, upper)
    else:
      main_serial(lower, upper)

  else:
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

