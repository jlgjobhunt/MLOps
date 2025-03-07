# ./MLOps/xarray/xarray.install.test0.py

import matplotlib
matplotlib.use('Agg')
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

def demonstrate_xarray_usage():
    """
    Demonstrates basic xarray usage: creating, manipulating, and plotting.
    """

    try:
        # 1. Create a DataArray (multi-dimensional array with labels).
        data = np.random.rand(4,3)
        coords = {'x': [10, 20, 30, 40], 'y': ['a', 'b', 'c']}
        da = xr.DataArray(data, coords=coords, dims=('x', 'y'), name='my_data')

        print("DataArray:\n", da)

        # 2. Perform operations (example: calculate the mean along one dimension)
        da_mean_x = da.mean(dim='x')
        print("\nMean along x-axis:\n", da_mean_x)

        # 3. Select data using labels (powerful feature of xarray)
        da_subset = da.sel(x=slice(20, 40), y=['a', 'c'])
        print("\nSubset of DataArray:\n", da_subset)

        # 4. Plotting (optional, but very common with xarray)
        da.plot()
        plt.title("Xarray DataArray Plot")
        
        plt.savefig("xarray_plot.png")
        plt.savefig("xarray_plot.pdf")
        plt.savefig("xarray_plot.jpg")

        print("Plot saved to xarray_plot.png")

        # More advanced plotting examples (uncomment if needed).
        # da.plot.line(x='x')
        # da.plot.imshow()

        print("\nXarray usage demonstrated successfully.")
        return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    demonstrate_xarray_usage()

