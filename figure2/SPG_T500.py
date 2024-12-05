#!/usr/bin/env python

import cf
import numpy as np
import matplotlib.pyplot as plt
import plot_styles as ps
from scipy.stats import linregress

def plot_spg_t500(ax):
    dir='/home/users/dlrhodso/CANARI/SPRINT_2024/analysis/SPG/'
    # 1. Load ensemble data files for `SOPHTADV_ATL_26_0_ANN` and `SOPHTLDF_ATL_26_0_ANN`

    data=cf.read(dir+'spg_t500/spg_*.nc')



    spg_s500=data.select_by_ncvar("spg_T500_ann")


    total_26_ann_list = []
    slope_list = []
    for member in spg_s500:

       
        this_realization=member.properties()['realization_index']

        #find members that have max an min trend 1980-2014
        ## CHECK WE DON't MEAN 2015-01-01!!
        total_sub=member.subspace(time=cf.wi(cf.dt("1980-01-01"), cf.dt("2014-01-01")))
        slope, intercept, r_value, p_value, std_err = linregress(total_sub.coord('time').array, total_sub.array)
        slope_list.append(slope)
        total_26_ann_list.append(member)


        
    #locate the max and min slope members
    min_slope_member=total_26_ann_list[np.argmin(slope_list)]
    max_slope_member=total_26_ann_list[np.argmax(slope_list)]


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
    ax.set_ylim(6, 9)

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
    ax.set_ylabel("SPG T500 (C)")
    #ax.legend()

# Test the function by plotting it independently
if __name__ == "__main__":
     fig, ax = plt.subplots()
     plot_spg_t_500(ax)
     plt.show()
