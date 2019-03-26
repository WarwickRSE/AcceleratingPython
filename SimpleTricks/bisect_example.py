from timeit import default_timer as timer
import numpy as np
import bisect
import sys

def generate_lists(n_elements = 10000000):
    l = np.random.rand(n_elements)
    l.sort()
    return l

def find_in(list, value):
    return value in list

def find_bisect(list, value):
    return bisect.bisect_left(list, value)

def main(num_items, n_reps):

    l = generate_lists(num_items)
    rel = [np.random.randint(0, num_items) for el in range(n_reps)]

    print("Time to find random element with in")
    start = timer()
    for i in range(n_reps):
        v = find_in(l, l[rel[i]])
    end = timer()
    print("Average time is ", (end-start)/n_reps)

    print("")

    print("Time to find random element with bisect")
    start = timer()
    for i in range(n_reps):
        v = find_bisect(l, l[rel[i]])
    end = timer()
    print("Average time is ", (end-start)/n_reps)
        

if __name__ == "__main__":

  try:
    num_items = int(sys.argv[1])
    n_reps = int(sys.argv[2])
  except:
    num_items = 10000000
    n_reps = 10

  print("Using ", num_items, "items averaged over ", n_reps)
  main(num_items,n_reps)

