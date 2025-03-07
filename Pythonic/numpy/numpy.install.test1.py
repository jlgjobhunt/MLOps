import numba.cuda
import numpy as np
import altair as alt
import pandas as pd
import time

# The kernel.
@numba.cuda.jit(cache=False)
def c_kernel(data, out):
    i = numba.cuda.threadIdx.x + numba.cuda.blockIdx.x * numba.cuda.blockDim.x
    if i < data.size:
        out[i] = data[i] * 2

data_size = 1024 * 1024
data = np.arange(data_size, dtype=np.int32)
out = np.zeros_like(data)

d_data = numba.cuda.to_device(data)
d_out = numba.cuda.to_device(out)

threads_per_block = 256

# The number of CUDA cores in an Nvidia Quadro M1200 has.
number_of_cuda_cores = 640

# Verify initial data transfer.
h_data_check = d_data.copy_to_host()
print("First 10 elements on device:", h_data_check[:10])


# Key Change: Increased number of blocks.
blocks = (data_size + threads_per_block -1) // threads_per_block
blocks = max(128, blocks)

start_time = time.time()
c_kernel[blocks, threads_per_block](d_data, d_out)
numba.cuda.synchronize()
end_time = time.time()

out = d_out.copy_to_host()

print(f"CUDA kernel executed in in {end_time - start_time:.6f} seconds.")

# Run the kernel multiple times.
num_iterations = 10

# Repeat the entire benchmark several times.
num_runs = 5

# Block counts experiment

all_results = []

for blocks in [128, 160, 192, 224, 256, 512, 1024, 2048]:
    results = []
    for _ in range(num_runs):
    
        start_time = time.perf_counter()

        for _ in range(num_iterations):
            c_kernel[blocks, threads_per_block](d_data, d_out)
            numba.cuda.synchronize()    

        end_time = time.perf_counter()
        time_per_iteration = (end_time - start_time) / num_iterations
        results.append(time_per_iteration)

    average_time = sum(results) / num_runs
    all_results.append({"blocks": str(blocks), "average_time": average_time})


# Transfer result back to host.
out = d_out.copy_to_host()

# Verify kernel output.
print("First 10 elements of output:", out[:10])

# Create a Pandas DataFrame from the results.
df = pd.DataFrame(all_results)

# Create the Altair chart.
chart = alt.Chart(df).mark_line(point=True).encode(
    x="blocks:O",
    y="average_time:Q",
    tooltip=["blocks", "average_time"]
).properties(
    title="CUDA Kernel Performance vs. Number of Blocks"
)

chart.show()
chart.save("chart.html")
chart.save("chart.png")
