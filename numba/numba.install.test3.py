# .MLOps/numba/numba.install.test3.py

import numpy as np
import time
from numba import cuda

# CUDA kernel (runs on the GPU)
@cuda.jit

def array_sum_cuda(arr, result):
    """
    array_sum_cuda(arr, result) --> array
    The array stores the sum.
    """
    i = cuda.grid(1)
    stride = cuda.gridsize(1)

    local_sum = 0
    for j in range(i, arr.size, stride):
        local_sum += arr[j]

    # Atomic addition to avoid race conditions.
    cuda.atomic.add(result, 0, local_sum)

# --- Main execution. ---
array_size = 1000000

# Create a NumPy array on the host (CPU).
arr_host = np.arange(array_size, dtype=np.int64)

# Transfer the array to the device (GPU).
arr_device = cuda.to_device(arr_host)

# Create a result array on the device (initialized to 0).
result_device = cuda.to_device(np.array(np.array([0], dtype=np.int64)))


# Set up the grid and block dimensions (adjust as needed).
# Experiment with value as Nvidia card can support different
# counts of CUDA cores and CUDA threads.
# My device supports up to 640 CUDA cores.
# 
threads_per_block = 256
blocks_per_grid = (array_size + threads_per_block - 1)


# Time the CUDA kernel execution.
start_time = time.time()
array_sum_cuda[blocks_per_grid, threads_per_block](arr_device, result_device)
cuda.synchronize()
end_time = time.time()
print(f"CUDA version time: {end_time - start_time:.6f} seconds")


# Transfer the result back to the host.
result_host = result_device.copy_to_host()

print(f"CUDA Result: {result_host[0]}")
print(f"Python Result: {np.sum(arr_host)}")

assert np.sum(arr_host) == result_host[0], "Results don't match!"