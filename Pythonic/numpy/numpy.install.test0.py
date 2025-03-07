# ./MLOps/numpy/numpy.install.test0.py

import numpy as np

def confirm_numpy_installation():
    """
    Confirms NumPy installation by performing some basic array operations.
    """
    try:
        # Create a NumPy array.
        arr = np.array([1, 2, 3, 4, 5])
        print("NumPy array created:", arr)

        # Perform some operations.
        mean = np.mean(arr)
        print("Mean of the array:", mean)

        squared = arr**2
        print("Squared elements:", squared)

        reshaped = arr.reshape(5, 1) # Reshape to a column vector.
        print("Reshaped array:\n", reshaped)

        matrix = np.array([[1,2], [3,4]])
        inverse = np.linalg.inv(matrix)
        print("Inverse of matrix:\n", inverse)

        print("NumPy installation confirmed successfully!")

    except ImportError:
        print("Error: NumPy is not installed.")
    except AttributeError as e:
        # Catch NumPy-specific errors.
        print(f"NumPy Attribute Error: {e}.")
    except Exception as e:
        print(f"An unexpected error occurrred: {e}.")

if __name__ == "__main__":
    confirm_numpy_installation()