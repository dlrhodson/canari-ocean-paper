#!/usr/bin/env python
import matplotlib.pyplot as plt
import sys
import os
#add current directory to the import path
sys.path.append(os.getcwd())

# Import the functions from external scripts (assuming you have them saved as `panel_a.py`, etc.)
# Each script should contain a function that generates or plots the respective panel data
from AMOC_26N import plot_amoc_timeseries
from plot_amoc_ensemble import plot_amoc_2d
from AHT_26N import plot_atlantic_ht_26n
from AST_26N import plot_atlantic_st_26n
# plot style parameters in plot_styles.py




# Create a figure and a 2x2 grid of subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Flatten axes array for easy indexing and looping
axes = axes.flatten()

# Define the function calls for each panel
plot_functions = [plot_amoc_timeseries, plot_amoc_2d, plot_atlantic_ht_26n ,  plot_atlantic_st_26n]

# Loop through each panel, plot the data, and add labels
for i, (ax, plot_func) in enumerate(zip(axes, plot_functions)):
    print(plot_func.__name__)
    plot_func(ax)  # Call the plotting function for each panel, passing the axis to plot on
     # Add the label in the top left corner, bold and 50% larger
    ax.text(
        0.025, 0.975, f"{chr(97 + i)})", 
        transform=ax.transAxes, 
        fontsize='x-large',  # This makes it 50% larger than the default size
        fontweight='bold', 
        va='top', ha='left'
    )
    #ax.set_title(f"{chr(97 + i)})")  # Adds labels 'a)' to 'd)' to each panel in the corner

# Adjust layout to avoid overlap
plt.tight_layout()

# Add script path as text below x-axis
script_path = os.path.abspath(__file__)
plt.figtext(0.5, 0.985, f"{script_path}", ha='center', fontsize=8)

plt.show()
