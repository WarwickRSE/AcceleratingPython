import matrix
from timeit import default_timer
import numpy as np

start = default_timer()
a=matrix.gen_random_matrices()
end = default_timer()

print('Generate matrix ', end-start)

start = default_timer()
b=matrix.multiply_matrices(a)
print(np.amax(b))
end = default_timer()

print('Multiply Matrix ', end-start)

#Run the jit versions once to compile the code
a=matrix.gen_random_matrices()
b=matrix.multiply_matrices(a)

import matrix_jit as matrix
start = default_timer()
a=matrix.gen_random_matrices()
end = default_timer()

print('Generate matrix ', end-start)

start = default_timer()
b=matrix.multiply_matrices(a)
print(np.amax(b))
end = default_timer()

print('Multiply Matrix ', end-start)
