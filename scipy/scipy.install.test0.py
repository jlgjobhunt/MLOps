# ./MLOps/scipy/scipy.install.test0.py

import scipy
import numpy as np

def check_scipy_installation():
    """
    Confirms SciPy installation and basic functionality.
    """

    try:
        # Check version.
        print(f"SciPy version: {scipy.__version__}")

        # Basic functionality test (using a function from a common module)
        from scipy.optimize import minimize
        result = minimize(lambda x: x**2, 0)
        print(f"Optimization result: {result.fun}")

        # Check for specific modules (optional)
        from scipy import stats
        print("SciPy stats module imported successfully.")
        print("SciPy installation confirmed.")
        return True
    
    except ImportError:
        print("SciPy is not installed.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
if __name__ == "__main__":
    check_scipy_installation()