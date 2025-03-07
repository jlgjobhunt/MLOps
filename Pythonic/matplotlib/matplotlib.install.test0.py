# ./MLOps/matplotlib.install.test0.py

import matplotlib
matplotlib.use('Agg')  # To avoid Wayland errors.
import matplotlib.pyplot as plt
import numpy as np

def confirm_matplotlib_installation():
    """
    Confirm Matplotlib installation by generating and displaying a simple plot.
    """

    try:

        # Generate some sample data.
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Create a plot.
        plt.plot(x, y)

        # Add labels and title.
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Matplotlib Installation Confirmation")

        # Display the plot.
        plt.show()

        print("Matplotlib installation confirmed successfully.")

    except ImportError:
        print("Error: Matplotlib is not installed.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    confirm_matplotlib_installation()