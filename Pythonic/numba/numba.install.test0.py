# .MLOps/numba/numba.install.test0.py

import numba.cuda

try:
    # Get the device (if a CUDA-enabled GPU is present).
    device = numba.cuda.get_current_device()

    # Print device information.
    print(f"Device Name: {device.name}")
    print(f"Compute Capability: {device.compute_capability}")
    print(f"Driver Version: {numba.cuda.cudadrv.driver.get_version()}")

    # A simple CUDA kernel test (important!).
    @numba.cuda.jit
    def cuda_test_kernel():
        i = numba.cuda.grid(1)
        if i == 0:
            print("CUDA kernel executed successfully!")

    # Launch with 32 blocks and 128 threads per block.
    cuda_test_kernel[128, 128]()
    numba.cuda.synchronize()

except numba.cuda.cudadrv.runtime.CudaSupportError as e:
    print(f"CUDA Support Error: {e}")
    print("Check your CUDA installation and driver.")

except ValueError as e:
    print(f"No CUDA device found: {e}")
    print("Make sure you have a CUDA-enabled GPU and the correct drivers installed.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")