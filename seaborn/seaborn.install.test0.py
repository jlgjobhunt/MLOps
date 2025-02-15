# ./MLOps/seaborn/seaborn.install.test0.py

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def check_seaborn_installation():
    """
    Confirms Seaborn installation and basic plotting functionality.
    """

    try:
        # Check version.
        print(f"Seaborn version: {sns.__version__}")

        # Basic plotting functionality test (using a sample dataset).
        # Create a sample DataFrame (replace with your data if needed).
        data = {'col1': [1, 2, 3, 4, 5],
                'col2': [2, 4, 1, 3, 5],
                'col3': [5, 4, 3, 2, 1]}
        df = pd.DataFrame(data)

        # Create a simple scatter plot.
        sns.scatterplot(x='col1', y='col2', data=df)
        plt.title('Seaborn Scatter Plot Test')
        plt.show()

        print("Seaborn installation confirmed.")
        return True
    
    except ImportError:
        print("Seaborn is not installed.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
if __name__ == "__main__":
    check_seaborn_installation()