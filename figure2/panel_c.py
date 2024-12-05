# panel_a.py

import matplotlib.pyplot as plt
import numpy as np

def plot_panel_c(ax):
    """
    Plot a simple test graph on the provided Axes object for panel A.

    Parameters:
    ax (matplotlib.axes.Axes): The axis to plot on.
    """
    # Generate some example data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Plot the data
    ax.plot(x, y, label="sin(x)")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_title("Panel A: Sine Wave")
    ax.legend()

# Test the function by plotting it independently
if __name__ == "__main__":
    fig, ax = plt.subplots()
    plot_panel_a(ax)
    plt.show()
