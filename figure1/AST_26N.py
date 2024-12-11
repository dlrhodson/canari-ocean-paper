#!/usr/bin/env python



import cf
import numpy as np
import matplotlib.pyplot as plt
import plot_styles as ps
from scipy.stats import linregress
import json
from matplotlib.ticker import MultipleLocator, FixedLocator

def plot_atlantic_st_26n(ax):
    dir='/home/users/dlrhodso/CANARI/SPRINT_2024/analysis/Salt_Transport/'
    # 1. Load ensemble data files for `SOPSTADV_ATL_26_0_ANN` and `SOPSTLDF_ATL_26_0_ANN`


    
    data=cf.read(dir+'Atl_ST_26.0/Atl_ST_26.0_*_sopstadv_atl.nc')

    #read in members with max min AMOC 26N trends over 1980-2014
    with open("amoc_26N_limits.json", "r") as file:
        maxmin = json.load(file)
        smax = maxmin["smax"]
        smin = maxmin["smin"]


    # 2. Load RAPID dataset
    #rapid_data = cf.read(dir+'RAPID_MHT_26N_ann_mean.nc')[0]

    # 3. Define a new time axis with 15 points, from "15-JUL-2005" to "15-JUL-2019"
    ##time_axis = cf.DimensionCoordinate()
    ##time_axis.set_properties({'units': 'days since 2005-07-15', 'calendar': '360_day'})
    ##time_axis.bounds(cf.Bounds(np.linspace(0, 14*360, 15)))

    # 4. Calculate total annual data (`total_26_ann`)
    # Assumes data is structured so that `SOPHTADV_ATL_26_0_ANN` and `SOPHTLDF_ATL_26_0_ANN` 
    # can be added directly from each ensemble member's data

    advective=data.select_by_ncvar("sopstadv_atl_26_0_ann")
    diffusive=data.select_by_ncvar("sopstldf_atl_26_0_ann")

    total_26_ann_list = cf.FieldList()
    slope_list = []
    for member in advective:

        sopstadv = member.squeeze()
        this_realization=member.properties()['realization_index']
        this_ldf=diffusive.select_by_property(realization_index=this_realization)
        if len(this_ldf)!=1:
            print("Something went wrong!")
            import pdb; pdb.set_trace()

        sopstldf = this_ldf[0].squeeze()
        total_26_ann = sopstadv + sopstldf
        #find members that have max an min trend 1980-2014
        ## CHECK WE DON't MEAN 2015-01-01!!
        total_sub=total_26_ann.subspace(time=cf.wi(cf.dt("1980-01-01"), cf.dt("2014-01-01")))
        slope, intercept, r_value, p_value, std_err = linregress(total_sub.coord('time').array, total_sub.array)
        slope_list.append(slope)
        total_26_ann_list.append(total_26_ann)


        
    #locate the max and min slope members
    #min_slope_member=total_26_ann_list[np.argmin(slope_list)]
    #max_slope_member=total_26_ann_list[np.argmax(slope_list)]
    #max min member from AMOC 26N now
    min_slope_member=total_26_ann_list.select_by_property(realization_index=str(smin))[0]
    max_slope_member=total_26_ann_list.select_by_property(realization_index=str(smax))[0]


    # Convert list to NumPy array for easy calculation across the ensemble
    total_26_ann_array = np.array(total_26_ann_list)
    time=total_26_ann_list[0].coord('time').year.array
    # 5. Calculate ensemble mean and standard deviation
    total_26_mean = np.mean(total_26_ann_array, axis=0)

    total_26_max=np.max(total_26_ann_array,axis=0)
    total_26_min=np.min(total_26_ann_array,axis=0)


    total_26_sd = np.std(total_26_ann_array, axis=0)
    total_26_high = total_26_mean + total_26_sd
    total_26_low = total_26_mean - total_26_sd

    


    # 6. Plot mean with one standard deviation spread
    #ax.fill_between(time, total_26_low, total_26_high, color=ps.spread_colour, label="1σ Spread")
    ax.fill_between(time, total_26_min, total_26_max, color=ps.spread_colour, label="range")
    
    #ax.title("Atlantic Heat Transport 26N PW 1σ Spread")
    ax.set_ylim(-65, -15)
    ax.set_xlim([ps.start_date.year, ps.end_date.year])
     # Set ticks every 10 years
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.xaxis.set_minor_locator(MultipleLocator(10))

    # Set labels every 20 years

    ax.plot(time,max_slope_member.array, label="max", color=ps.max_colour)
    ax.plot(time,min_slope_member.array, label="min", color=ps.min_colour)
    ax.plot(time,total_26_mean, label="Total 26N Mean", color=ps.mean_colour,lw=3)
    

    # 7. Overlay RAPID data (adjust units to match)
    #mht_26n_ann = rapid_data
    #rapid_time=rapid_data.coord('time').year.array
    #mht_26n_ann_rescaled = mht_26n_ann.array / 1e15
    #ax.plot(rapid_time,mht_26n_ann_rescaled, label="RAPID", color=ps.obs_colour, lw=3)

    # Add labels and legend
    #ax.set_xlabel("Time")
    ax.set_ylabel("Salt Transport (Gg/s)")
    #ax.legend()

# Test the function by plotting it independently
if __name__ == "__main__":
     fig, ax = plt.subplots()
     plot_atlantic_st_26n(ax)
     plt.show()
