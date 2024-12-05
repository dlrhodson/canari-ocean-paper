#!/usr/bin/env python



import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import seaborn
import os
import glob
import dask
import plot_styles as ps

import pandas as pd


def plot_spg_stream(ax):
    #fp = "/home/users/atb299/CANARI/Figures/"

    DO="/gws/nopw/j04/canari/users/atb299/"
    EM_psi_00_14_stats = xr.open_dataset(DO+"Ensemble_psi_stats.nc")

    EM_psi_00_14_stats_spg = EM_psi_00_14_stats.isel(x=slice(850,1200),y=slice(850,1100))

    EM_psi_00_14_stats_spg_ens = EM_psi_00_14_stats_spg['sobarstf_mean'].mean(dim="ensemble_member").to_dataset(name="sobarstf_emean")
    EM_psi_00_14_stats_spg_ens['sobarstf_min'] = EM_psi_00_14_stats_spg['sobarstf_mean'].min(dim="ensemble_member")
    EM_psi_00_14_stats_spg_ens['sobarstf_max'] = EM_psi_00_14_stats_spg['sobarstf_mean'].max(dim="ensemble_member")
    EM_psi_00_14_stats_spg_ens['sobarstf_std'] = EM_psi_00_14_stats_spg['sobarstf_mean'].std(dim="ensemble_member")
    EM_psi_00_14_stats_spg_ens['nav_lon'] = EM_psi_00_14_stats_spg['nav_lon']
    EM_psi_00_14_stats_spg_ens['nav_lat'] = EM_psi_00_14_stats_spg['nav_lat']
    EM_psi_00_14_stats_spg_ens = EM_psi_00_14_stats_spg_ens.set_coords(("nav_lat", "nav_lon"))

    #fig, axs = plt.subplots(2, 2, sharex =True, sharey = True, figsize=(16,10));

    (EM_psi_00_14_stats_spg_ens['sobarstf_emean']/1e6).plot(ax=ax,vmin=-50,vmax=5,cmap="Spectral",x="nav_lon",y="nav_lat",cbar_kwargs={'orientation': 'horizontal','label':'Sv'});
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    #(EM_psi_00_14_stats_spg_ens['sobarstf_std']/1e6).plot(ax=axs[0,1],vmax=3,x="nav_lon",y="nav_lat");
    #((EM_psi_00_14_stats_spg_ens['sobarstf_min']-EM_psi_00_14_stats_spg_ens['sobarstf_emean'])/1e6).plot(
     #   ax=axs[1,0],vmin=-5,vmax=0,cmap="Spectral",x="nav_lon",y="nav_lat");
    #((EM_psi_00_14_stats_spg_ens['sobarstf_max']-EM_psi_00_14_stats_spg_ens['sobarstf_emean'])/1e6).plot(
     #   ax=axs[1,1],vmin=0,vmax=5,cmap="Spectral_r",x="nav_lon",y="nav_lat");

    #ax.set_title("Ensemble and time mean");
    #axs[0,1].set_title("Ensemble standard deviation");
    #axs[1,0].set_title("Ensemble min - Ensemble time mean");
    #axs[1,1].set_title("Ensemble max - Ensemble time mean");

    xmin, xmax = -64, -5
    ymin, ymax = 45, 67
    ax.set_xlim([xmin, xmax]);
    ax.set_ylim([ymin, ymax]);

    #plt.savefig(fp+'Psi_2000-2014_mean_stats_C_LE_paper.png', dpi=300, transparent=False, bbox_inches='tight', pad_inches=0.1)

# Test the function by plotting it independently
if __name__ == "__main__":
     fig, ax = plt.subplots()
     plot_spg_stream(ax)
     plt.show()
