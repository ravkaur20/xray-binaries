import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io import fits
import glob

#when running this file, the first input (python3.9 -thisfile-.py input1) should be the path to the directory in which the files are
directory = sys.argv[1]
#binsize = sys.argv[2]

source_directories = sorted(glob.glob(f'{directory}/my_source*/'))

#for source in source_directories:
    #cmd = "sh lc_filemaker_bkg.sh " + source + " " + binsize
    #print(cmd)
    #os.system(cmd)

for source in source_directories:
    os.chdir(source)
    broad_files = sorted(glob.glob(f'{source}/*b.lc.txt'))
    soft_files = sorted(glob.glob(f'{source}/*s.lc.txt'))
    medium_files = sorted(glob.glob(f'{source}/*m.lc.txt'))
    hard_files = sorted(glob.glob(f'{source}/*h.lc.txt'))
    bintime_files = sorted(glob.glob(f'{source}/*bintime.txt'))
    directory_name = os.path.basename(source.rstrip('/'))

    all_files = np.stack((broad_files, soft_files, medium_files, hard_files, bintime_files), axis=1)

    durations = []

    for file in all_files:

        broad_data = np.loadtxt(file[0])
        soft_data = np.loadtxt(file[1])
        medium_data = np.loadtxt(file[2])
        hard_data = np.loadtxt(file[3])

        data_stack = np.stack((broad_data, soft_data, medium_data, hard_data), axis=1)
        
        filtered = []
        for idx, data_stack_i in enumerate(data_stack):
            array = data_stack[idx]
            if array[0][4] != 0:
                filtered.append(array)
        filtered_new = np.array(filtered)

        bd = filtered_new[:,0]

        min_time = bd[:,0].min()
        max_time = bd[:,0].max()
        durations.append(max_time - min_time)
    
    max_duration = max(durations)/1000

    for file in all_files:

        broad_data = np.loadtxt(file[0])
        soft_data = np.loadtxt(file[1])
        medium_data = np.loadtxt(file[2])
        hard_data = np.loadtxt(file[3])
        bintime = np.loadtxt(file[4])

        data_stack = np.stack((broad_data, soft_data, medium_data, hard_data), axis=1)
        
        filtered = []
        for idx, data_stack_i in enumerate(data_stack):
            array = data_stack[idx]
            if array[0][4] != 0:
                filtered.append(array)
        filtered_new = np.array(filtered)

        bd = filtered_new[:,0]
        sd = filtered_new[:,1]
        md = filtered_new[:,2]
        hd = filtered_new[:,3]

        min_time = bd[:,0].min()
        time_data = (bd[:,0] - min_time)/1000

        obsid = file[0][-41:-36]
        regid = file[0][-26:-22]

        fig, axs = plt.subplots(2, 1, figsize=(10,6), constrained_layout = True, sharey = True)

        axs[0].errorbar(time_data, bd[:,1], yerr=bd[:,2], color = 'red', marker = 'o', markerfacecolor = 'black', markersize = 4, ecolor = 'black', markeredgecolor = 'black', capsize=3)
        axs[0].set_xlim([0, 70])

        axs[1].plot(time_data, sd[:,1], color='red', label='Soft')
        axs[1].plot(time_data, md[:,1], color='green', label='Medium')
        axs[1].plot(time_data, hd[:,1], color = 'blue', label='Hard')
        axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, frameon = False, fontsize = 14)
        axs[1].set_xlim([0, 70])

        fig.supylabel('Net Count Rate (Counts/Second)')
        fig.supxlabel('Time (ks)')
        fig.suptitle(f'Background corrected lightcurve for: {directory_name}, ObsID {obsid}, RegID {regid} with {bintime}s Bin size')
        plt.savefig(f'{source}/{directory_name}_{obsid}_reg{regid}_bkg_corrected_lc_img.png', dpi=200, bbox_inches='tight')
        plt.close()
