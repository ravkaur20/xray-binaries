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

#source_directories = sorted(glob.glob(f'{directory}/2CXO*/'))
source_directories = sorted(glob.glob(f'{directory}/bkg*/'))

#for source in source_directories:
    #os.chdir(source)
    #os.system('gunzip *.gz')

#for source in source_directories:
    #cmd = "sh lc_filemaker.sh " + source + " " + binsize
    #print(cmd)
    #os.system(cmd)

for source in source_directories:
    os.chdir(source)
    broad_files = sorted(glob.glob(f'{source}/*evt3.fits.b.lc.txt'))
    soft_files = sorted(glob.glob(f'{source}/*evt3.fits.s.lc.txt'))
    medium_files = sorted(glob.glob(f'{source}/*evt3.fits.m.lc.txt'))
    hard_files = sorted(glob.glob(f'{source}/*evt3.fits.h.lc.txt'))
    #bintime_files = sorted(glob.glob(f'{source}/*bintime.txt'))
    #directory_name = os.path.basename(source.rstrip('/'))

    all_files = np.stack((broad_files, soft_files, medium_files, hard_files), axis=1)
    #all_files = np.stack((broad_files, bintime_files), axis=1)

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
        #bintime = np.loadtxt(file[1])

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
        #obsid = file[0][-30:-25]
        #regid = file[0][-26:-22]

        df = pd.DataFrame({'Time': time_data, 'Net Count Rate': bd[:,1], 'Soft': sd[:,1], 'Medium': md[:,1], 'Hard': hd[:,1]})
        df_rolling = df.rolling(window=3, center=True).mean()
        rolling_std = df.rolling(window=3, center=True).std()

        fig, axs = plt.subplots(3, 1, figsize=(10,6), constrained_layout = True, sharey = True)

        axs[0].errorbar(time_data, bd[:,1], yerr=bd[:,2], color = 'red', marker = 'o', markerfacecolor = 'black', markersize = 4, ecolor = 'black', markeredgecolor = 'black', capsize=3)
        axs[0].set_xlim([0, max_duration])
        
        #axs[1].errorbar(df_rolling['Time'], df_rolling['Net Count Rate'], yerr = rolling_std['Net Count Rate'], color = 'red', marker = 'o', markerfacecolor = 'black', markersize = 4, ecolor = 'black', markeredgecolor = 'black', capsize=3)
        axs[1].plot(df_rolling['Time'], df_rolling['Net Count Rate'], color = 'red', marker = 'o', markerfacecolor = 'black', markeredgecolor = 'black', markersize = 3)
        axs[1].set_xlim([0, max_duration])

        axs[2].plot(df_rolling['Time'], df_rolling['Soft'], color='red', label='Soft')
        axs[2].plot(df_rolling['Time'], df_rolling['Medium'], color='green', label='Medium')
        axs[2].plot(df_rolling['Time'], df_rolling['Hard'], color = 'blue', label='Hard')
        axs[2].legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, frameon = False, fontsize = 14)
        axs[2].set_xlim([0, max_duration])

        fig.supylabel('Count Rate (Counts/Second)')
        fig.supxlabel('Time (ks)')
        fig.suptitle(f'BC Rolling Lightcurve for ObsID {obsid}, with 100s Bin size')
        plt.savefig(f'bc_rolling_100sec_lc_{obsid}.png', dpi=200, bbox_inches='tight')
