# ./MLOps/dask/dask.install.test0.py

import dask.array as da 
import numpy as np
import time
import graphviz

# Create a large Dask array (distributed across chunks).
# Simulate a large dataset.
chunk_size = 1000 # Adjust chunk size as needed.
array_size = 100000 # Make it a bigger number to see the difference.
data = np.random.rand(array_size)
dask_array = da.from_array(data, chunks=(chunk_size,))

# Perform some computations (example: calculate the mean and standard deviation).

start_time = time.time()
mean = dask_array.mean().compute() # .compute() is crucial to trigger the computation
end_time = time.time()
print(f"Dask Mean Calculation Time: {end_time - start_time:.4f} seconds")

start_time = time.time()
std = dask_array.std().compute()
end_time = time.time()
print(f"Dask Std Calculation Time: {end_time - start_time:.4f} seconds.")

# More complex computations (example: element-wise square and sum).
start_time = time.time()
squared_sum = (dask_array**2).sum().compute()
end_time = time.time()
print(f"Dask Squared Sum Calculation Time: {end_time - start_time:.4f} seconds")

# Demonstrate delayed computation.
# This is a key feature of Dask: building up a task graph before execution.
delayed_mean = dask_array.mean() # No .compute() here!
delayed_std = dask_array.std()

# At this point, no computation has happened. Dask has built a graph
# of the operations. We can inspect the graph:
delayed_mean.visualize()
# Uncomment to visualize the task graph (requires graphviz)

# Now, trigger the computations of both mean and std at once (more efficient).
start_time = time.time()
mean, std = da.compute(delayed_mean, delayed_std) # Compute both together.
end_time = time.time()
print(f"Dask Combined Mean/Std Calculation Time: {end_time - start_time:.4f} seconds")

print(f"Mean: {mean}")
print(f"Standard Deviation: {std}")
print(f"Squared Sum: {squared_sum}")

# Example of filtering and aggregation.
start_time = time.time()
filtered_array = dask_array[dask_array > 0.5] # Filter elements > 0.5
filtered_sum = filtered_array.sum().compute()
end_time = time.time()
print(f"Dask Filtered Sum Calculation Time: {end_time - start_time:.4f} seconds")
print(f"Filtered Sum: {filtered_sum}")

# Using Dask with Pandas (if you have tabular data).
import dask.dataframe as dd
import pandas as pd

df = pd.DataFrame({'A': np.random.randint(0, 10, size=array_size), 'B': np.random.rand(array_size)})
ddf = dd.from_pandas(df, npartitions=4) # Partition the DataFrame

start_time = time.time()
grouped_mean = ddf.groupby('A')['B'].mean().compute()
end_time = time.time()
print(f"Dask Grouped Mean Calculation Time: {end_time - start_time:.4f} seconds")
print(f"Grouped Mean: \n{grouped_mean}")



