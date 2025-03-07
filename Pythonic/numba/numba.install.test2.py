# .MLOps/numba/numba.install.test2.py

import numpy as np
import time
from numba import jit

# Pure Python version (slow)
def array_sum_python(arr):
    total = 0
    for i in range(arr.size):
        total += arr[i]
    return total

# Numba JIT compiled version (fast)
@jit(nopython=True)
def array_sum_numba(arr):
    total = 0
    for i in range(arr.size):
        total += arr[i]
    return total

# --- Main execution ---
array_size = 1000000

# Create a NumPy array
arr = np.arange(array_size)

# Time the Python version
start_time = time.time()
result_python = array_sum_python(arr)
end_time = time.time()
print(f"Python version time: {end_time - start_time:.6f} seconds")

# Time the Numba version (first call compiles, so time it twice)
start_time = time.time()
result_numba = array_sum_numba(arr)
end_time = time.time()
print(f"Numba (first call) time: {end_time - start_time:.6f} seconds")

start_time = time.time()
result_numba = array_sum_numba(arr)
end_time = time.time()
print(f"Numba (second call) time: {end_time - start_time:.6f} seconds")


print(f"Python Result: {result_python}")
print(f"Numba Result: {result_numba}")
assert result_python == result_numba, "Results don't match!"