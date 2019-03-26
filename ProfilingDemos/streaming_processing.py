
import time
from numpy import random as nprandom
from sys import argv
from math import exp

def generate_data():


  #Setting n_els to 1 billion will hit 8GB of data

  n_els = 1000000
  print("Generating ", n_els, "random values")
  dat = nprandom.rand(n_els)

  with open('data_for_streaming_test.txt', 'w') as outfile:
    for i in range(1, n_els):
      outfile.write(str(dat[i])+'\n')

def read_data(convert=True):

  data = []
  with open("data_for_streaming_test.txt") as infile:
    data = infile.readlines()
  if convert: data = [float(el) for el in data]
  return data

def pre_read_total():

  convert = False
  total = 0.0
  data = read_data(convert=convert)
  if convert:
    for el in data:
      total += el
  else:
    for el in data:
      total += float(el)

  return total

def streaming_total():

  total = 0.0
  with open("data_for_streaming_test.txt") as infile:
    el = infile.readline()
    while el != "":
      total += float(el)
      el = infile.readline()
  return total


def pre_read_heavier_processing():

  convert = False
  result = 0.0
  data = read_data(convert=convert)
  if convert:
    for el in data:
      result += exp(-(el-0.5)**2/0.25)
  else:
    for el in data:
      result += exp(-(float(el)-0.5)**2/0.25)

  return result

def streaming_heavier_processing():

  result = 0.0
  with open("data_for_streaming_test.txt") as infile:
    el = infile.readline()
    while el != "":
      result += exp(-(float(el)-0.5)**2/0.25)
      el = infile.readline()
  return result

def main(use_method = 0):

  try:
    infile = open("data_for_streaming_test.txt", 'r')
  except:
    #Generate data if it doesn't exist
    print("Data file not found, generating data")
    generate_data()

  #Randomly choose ordering and try to disrupt possible caching
  # between attempts

  a = nprandom.rand(1)
  #Enforce selected method if given
  if use_method == 1: a = 0.6
  if use_method == 2: a = 0.3

  if a > 0.5:
    start = time.time()
#    print(streaming_total())
    print(streaming_heavier_processing())
    end = time.time()
    print("Streaming version took {:.3e} s".format(end-start))

  else:
    start = time.time()
#    print(pre_read_total())
    print(pre_read_heavier_processing())
    end = time.time()
    print("Pre-read version took {:.3e} s".format(end-start))

if __name__ == "__main__":

  import cProfile as prof
  import pstats

  try:
    use_method = int(argv[1])
  except:
    use_method = 0

  #Use the profiler class version not string so we can pass args
  pr = prof.Profile()
  pr.enable()
  main(use_method=use_method)
  pr.disable()
  pstats.Stats(pr).sort_stats("cumtime").print_stats()

