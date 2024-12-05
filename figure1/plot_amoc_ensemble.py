#!/usr/bin/env python

import os
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def y_scaling(y):
    """
    Apply sigma scaling transformation to stretch y-axis towards 38.
    """
    return np.power((y - 30) / (38 - 30), 2) * (38 - 30) + 30

def plot_amoc_2d(ax,output_dir='/home/users/dlrhodso/CANARI/SPRINT_2024/analysis/Niamh/AMOC_Sigma_Means'):
    """
    Plot AMOC ensemble data.

    Parameters:
    output_dir (str): Path to the directory containing time-mean files.
    """
    # Load all time-mean files
    files = sorted(glob.glob(os.path.join(output_dir, "member_*_time_mean.nc")))
    if not files:
        raise ValueError(f"No time-mean files found in directory: {output_dir}")

    datasets = [xr.open_dataset(f) for f in files]
    combined = xr.concat(datasets, dim='ensemble_member')
    lats = xr.open_dataset('/gws/nopw/j04/acsis/nboc20/outputs/mocsig/sigma_2000_fix/lats.nc').to_dataarray().squeeze()


    # Compute ensemble mean and standard deviation
    amoc_mean = combined.mean(dim='ensemble_member').to_dataarray().squeeze()[:,1:-1]
    amoc_std = combined.std(dim='ensemble_member').to_dataarray().squeeze()[:,1:-1]


    # Transform y-axis
    y_transformed = y_scaling(combined.sigma)
    yticks = np.linspace(30, 37, 8)
    yticks_transformed = y_scaling(yticks)

    # Plot
    ax.grid(alpha=0.3)
    ax.set_ylabel('$\sigma_2$')


    ccb = ax.pcolor(lats, y_transformed, amoc_std, cmap='viridis')
    ax.contour(lats, y_transformed, amoc_mean, levels=7, colors='grey', alpha=0.6)

    ax.set_yticks(np.delete(yticks_transformed,1), [f'{tick:.1f}' for tick in np.delete(yticks,1)])
    #ax.set_ylim([30, 36.5])
    ax.set_ylim([36.5,30])
    ax.set_xlim([-20,90])
    ax.set_xlabel('Latitude ($\degree$N)')
    #ax.set_title('Ensemble Std Dev AMOC')
    plt.gca().invert_yaxis()
    plt.colorbar(ccb, label='Standard Deviation (Sv)')


if __name__ == "__main__":
    fig, ax = plt.subplots()
    plot_amoc_2d(ax)
    plt.show()
