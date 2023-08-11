import os
import sys
import glob

#when running this file, the first input (python3.9 -thisfile-.py input1) should be the path to the directory in which the files are
directory = sys.argv[1]

source_directories = sorted(glob.glob(f'{directory}/2CXO*/'))

for source in source_directories:
    os.chdir(source)
    os.system('gunzip *.gz')
