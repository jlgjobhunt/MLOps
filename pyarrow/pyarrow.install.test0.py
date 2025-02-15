# ./MLOps/pyarrow/pyarrow.install.test0.py

import pyarrow as pa

def check_pyarrow_installation():
    """
    Confirms PyArrow installation and basic functionality.
    """

    try:
        # Check version
        print(f"PyArrow version: {pa.__version__}")

        # Basic functionality test (creating an array)
        arr = pa.array([1, 2, 3, 4, 5])
        print(f"PyArrow array:\n{arr}")

        # Perform a simple operation.
        arr_sum = arr.sum()
        print(f"Sum of array elements: {arr_sum}")

        # Check for specific modules/functionality (optional)
        print("PyArrow array created and manipulated successfully.")

        print("PyArrow installation confirmed.")
        return True
    
    except ImportError:
        print("PyArrow is not installed.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    check_pyarrow_installation()