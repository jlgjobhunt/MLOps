# ./MLOps/scikit-learn/scikit-learn.install.test0.py

import sklearn
import numpy as np

def check_sklearn_installation():
    """
    Confirms scikit-learn installation and basic functionality.
    """

    try:
        # Check version.
        print(f"Scikit-learn version: {sklearn.__version__}")

        # Basic functionality test (using a simple model).
        from sklearn.linear_model import LinearRegression
        X = np.array([[1,1], [1,2], [2,2], [2,3]])
        y = np.dot(X, np.array([1, 2])) + 3
        reg = LinearRegression().fit(X, y)
        score = reg.score(X, y)
        print(f"Linear Regression score: {score}")

        # Check for specific module (optional)
        from sklearn.metrics import mean_squared_error
        print("Mean Squared Error module imported successfully.")

        print("Scikit-learn installation confirmed.")
        return True
    
    except ImportError:
        print("Scikit-learn is not installed.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    

if __name__ == "__main__":
    check_sklearn_installation()

