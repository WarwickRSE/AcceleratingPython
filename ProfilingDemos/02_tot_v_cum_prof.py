import numpy as np


def find_simple_average(array):

  return np.mean(array)

def find_sliced_average(array, min_x_val):

  x_means = np.mean(array, axis=0)

  return np.mean(array[np.where(x_means > min_x_val),:], axis=1)

def processing(data):

  av = find_simple_average(data)

  av_half = find_sliced_average(data, 0.5)

def create_array():

  data = np.random.rand(50000, 5000)
  return data

def main():

  data = np.random.rand(50000, 5000)

  av = find_simple_average(data)

  av_half = find_sliced_average(data, 0.5)


if __name__ == "__main__":

  import cProfile as prof

  #prof.run("main()")
  prof.run("processing(create_array())")

