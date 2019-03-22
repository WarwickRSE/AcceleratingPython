import numpy as np

def gen_random_matrices():
    return (np.random.rand(10000,10000), np.random.rand(10000,10000))

def multiply_matrices(mat_tuple):
    return mat_tuple[0].dot(mat_tuple[1])
