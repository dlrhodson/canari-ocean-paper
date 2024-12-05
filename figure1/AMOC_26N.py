#!/usr/bin/env python



import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import seaborn
import os
import glob

import pandas as pd
import plot_styles as ps
import json



def plot_amoc_timeseries(ax):

    fp = "/home/users/atb299/CANARI/Figures/"


    def find_nearest(array,value):
        idx,val = min(enumerate(array), key=lambda x: abs(x[1]-value))
        return idx

    #Define paths and read data

    # Paths and ensemble members
    EXP="HIST2"
    OP="/gws/nopw/j04/canari/users/atb299/AMOC/"
    ENS=sorted(os.listdir(OP))

    #Open extracted AMOC variables - small files for ease of use

    EM_amoc_26N = xr.open_dataset(OP+"Ensemble_amoc_z_26N.nc").squeeze()
    EM_amoc_42N = xr.open_dataset(OP+"Ensemble_amoc_z_42N.nc").squeeze()
    EM_amoc_50N = xr.open_dataset(OP+"Ensemble_amoc_z_50N.nc").squeeze()
    EM_amoc_55N = xr.open_dataset(OP+"Ensemble_amoc_z_55N.nc").squeeze()

    z1k = find_nearest(EM_amoc_26N['depthw'],1000)
    EM_amoc_26N['zomsfatl_1k'] = EM_amoc_26N['zomsfatl'].isel(depthw=z1k)
    EM_amoc_42N['zomsfatl_1k'] = EM_amoc_42N['zomsfatl'].isel(depthw=z1k)
    EM_amoc_50N['zomsfatl_1k'] = EM_amoc_50N['zomsfatl'].isel(depthw=z1k)
    EM_amoc_55N['zomsfatl_1k'] = EM_amoc_55N['zomsfatl'].isel(depthw=z1k)

    # Annual, annual mean and variance
    EM_amoc_26N_annual = EM_amoc_26N.resample(time_counter='1Y').mean(dim='time_counter')
    EM_amoc_26N_annual['zomsfatl_1k_min'] = EM_amoc_26N_annual['zomsfatl_1k'].min(dim='ensemble_member') 
    EM_amoc_26N_annual['zomsfatl_1k_max'] = EM_amoc_26N_annual['zomsfatl_1k'].max(dim='ensemble_member') 
    EM_amoc_26N_annual['zomsfatl_1k_mean'] = EM_amoc_26N_annual['zomsfatl_1k'].mean(dim='ensemble_member') 
    EM_amoc_26N_annual['zomsfatl_1k_var'] = EM_amoc_26N_annual['zomsfatl_1k'].var(dim='ensemble_member')

    # Monthly mean and variance
    EM_amoc_26N['zomsfatl_1k_mean'] = EM_amoc_26N['zomsfatl_1k'].mean(dim='ensemble_member')
    EM_amoc_26N['zomsfatl_1k_var'] = EM_amoc_26N['zomsfatl_1k'].var(dim='ensemble_member')

    # Monthly seasonal cycle
    EM_amoc_26N['zomsfatl_1k_mean_scyc'] = EM_amoc_26N['zomsfatl_1k_mean'].groupby('time_counter.month').mean("time_counter")
    EM_amoc_26N['zomsfatl_1k_varmean_scyc'] = EM_amoc_26N['zomsfatl_1k_mean'].groupby('time_counter.month').var("time_counter")

    EM_amoc_26N['zomsfatl_1k_ensvar_as_scyc'] = EM_amoc_26N['zomsfatl_1k_var'].groupby('time_counter.month').mean("time_counter")


    # Ensemble with mean seasonal cycle removed
    EM_amoc_26N['zomsfatl_1k_anom'] = EM_amoc_26N['zomsfatl_1k'].groupby('time_counter.month') - EM_amoc_26N['zomsfatl_1k_mean_scyc'] # Remove mean seasonal cycle
    EM_amoc_26N['zomsfatl_1k_mean_anom'] = EM_amoc_26N['zomsfatl_1k_mean'].groupby('time_counter.month') - EM_amoc_26N['zomsfatl_1k_mean_scyc'] # Remove mean seasonal cycle

    # RAPID Obs
    Ramoc = xr.open_dataset('/gws/nopw/j04/canari/users/atb299/AMOC/moc_transports_2024-09.nc')
    Ramoc_M = Ramoc.resample(time='1M').mean() # Create monthly means - date assigned is last day of the month
    offset = pd.tseries.frequencies.to_offset("15D") # Use pandas to offset the assigned time to (approx.) centre of the month
    Ramoc_M["time"] = Ramoc_M.get_index("time") - offset # ...
    Ramoc_M['AMOC26_1k_sc'] = Ramoc_M['moc_mar_hc10'].groupby('time.month').mean("time")
    Ramoc_M['AMOC26_1k_sc_var'] = Ramoc_M['moc_mar_hc10'].groupby('time.month').var("time")
    Ramoc_M['AMOC26_1k_sc11on'] = Ramoc_M['moc_mar_hc10'].sel(time=slice('2011-01-01', '2022-12-31')).groupby('time.month').mean("time")
    Ramoc_M['AMOC26_1k_scpre10'] = Ramoc_M['moc_mar_hc10'].sel(time=slice('2004-04-01', '2009-12-31')).groupby('time.month').mean("time")

    Ramoc_Y = Ramoc.resample(time='1Y').mean() # Create annual means
    offset = pd.tseries.frequencies.to_offset("183D") # Use pandas to offset the assigned time to (apprx.) centre of the month
    Ramoc_Y["time"] = Ramoc_Y.get_index("time") - offset # ...

    # Convert to datetime64 format        
    Ramoc_M360 = Ramoc_M.convert_calendar(calendar = '360_day', align_on = 'date')
    Ramoc_Y360 = Ramoc_Y.convert_calendar(calendar = '360_day', align_on = 'date')

    # Bryden 2005 dots
    import cftime
    brydent = [cftime.Datetime360Day(1957,1,1), cftime.Datetime360Day(1981,1,1), cftime.Datetime360Day(1992,1,1), cftime.Datetime360Day(1998,1,1), cftime.Datetime360Day(2004,1,1)]
    brydena = [22.9, 18.7, 19.4, 16.1, 14.8]

    #Plot AMOC time series

    #EM_amoc_26N['zomsfatl_1k'][:,:].plot.line(hue='ensemble_member',size=6,aspect=2,add_legend=True);
    #EM_amoc_26N['zomsfatl_1k_mean'].plot(lw=3,color="white");
    #EM_amoc_26N['zomsfatl_1k_mean'].plot(lw=1,color="gray");
    #Ramoc_M360['moc_mar_hc10'][:].plot.line(label="RAPID",color='k')
    #seaborn.move_legend(plt.gca(), loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.title("AMOC @ 26N, 1 km: monthly time series for all ensemble members");
    #plt.savefig(fp+'AMOC26N_1k_monthly_ts.png', dpi=300, transparent=False, bbox_inches='tight', pad_inches=0.1)



    # Find strongest and weakest decline over 1980-2014
    slopes = EM_amoc_26N_annual['zomsfatl_1k'].sel(time_counter=slice("1980-01-01", "2014-01-01")).polyfit(dim="time_counter",deg=1)
    # AMOC is declining over this period, so smax == weakest decline, smin == strongest decline
    smax = slopes['polyfit_coefficients'][0].argmax()
    smin = slopes['polyfit_coefficients'][0].argmin()


    # Values to write
    data = {"smax": int(EM_amoc_26N_annual['ensemble_member'][int(smax)]), "smin":  int(EM_amoc_26N_annual['ensemble_member'][int(smin)])}

    # Write to a JSON file
    with open("amoc_26N_limits.json", "w") as file:
        json.dump(data, file)


    
    dt_min = slopes["polyfit_coefficients"][0,smin.values]*(34*365*86400*1e9)
    dt_max = slopes["polyfit_coefficients"][0,smax.values]*(34*365*86400*1e9)

    print("Strongest AMOC trend:",np.round(dt_min.values/3.4, 2), "Sv/decade")
    print("Weakest AMOC trend:  ",np.round(dt_max.values/3.4, 2), "Sv/decade")

    #Strongest AMOC trend: -1.64 Sv/decadea
    #Weakest AMOC trend:   -0.52 Sv/decade

    #fig,axs = plt.subplots(1, 1, figsize=(9,5))
    EM_amoc_26N_annual['zomsfatl_1k_mean'].plot(lw=3,color="white",ax=ax);
    ax.fill_between(EM_amoc_26N_annual['time_counter'].values, EM_amoc_26N_annual['zomsfatl_1k_min'].values,EM_amoc_26N_annual['zomsfatl_1k_max'].values,color=ps.spread_colour,label="C_LE range")
    ax.plot(EM_amoc_26N_annual['time_counter'],EM_amoc_26N_annual['zomsfatl_1k'][:,smax],color=ps.max_colour,label="C_LE min_trend");
    ax.plot(EM_amoc_26N_annual['time_counter'],EM_amoc_26N_annual['zomsfatl_1k'][:,smin],color=ps.min_colour,label="C_LE max_trend");
    ax.plot(EM_amoc_26N_annual['time_counter'],EM_amoc_26N_annual['zomsfatl_1k_mean'],color=ps.mean_colour,lw=3,label="C_LE mean");
    Ramoc_Y360['moc_mar_hc10'].plot.line(label="RAPID",color=ps.obs_colour,lw=3,ax=ax);
    ax.plot(brydent, brydena, 'ko',label="Bryden05")

    ax.set_xlabel("Year"); ax.set_ylabel("MOC (Sv)")
    #ax.legend();
    #plt.savefig(fp+'AMOC26N_1k_annual_ts_C_LE_paper.png', dpi=300, transparent=False, bbox_inches='tight', pad_inches=0.1)


# Test the function by plotting it independently
if __name__ == "__main__":
     fig, ax = plt.subplots()
     plot_amoc_timeseries(ax)
     plt.show()

