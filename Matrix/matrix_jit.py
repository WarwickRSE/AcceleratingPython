import numpy as np
from numba import jit

@jit
def gen_random_matrices():
    return (np.random.rand(10000,10000), np.random.rand(10000,10000))

@jit
def multiply_matrices(mat_tuple):
    return mat_tuple[0].dot(mat_tuple[1])
