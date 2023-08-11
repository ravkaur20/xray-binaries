import os
import sys

dt = float(sys.argv[1])

tdl = float(os.environ.get('tdl'))
#print(tdl)

#dt = 500
fdt = dt/tdl
ndt = int(fdt)
bintime = ndt*tdl

print(bintime)
