import pandas as pd
import os, sys
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
def read_csv(csv_filename):
    f = open(csv_filename)
    hdgs = []
    vels = []
    dats = []
    lats = []
    lons = []
    psss = []
    ssss = []
    dpts = []
    xxxs = []
    for line in f.readlines():
        line = line.strip().split(',')
        datetime = pd.to_datetime(line[1], dayfirst=True)
        hdr = line[0]
        if hdr == 'VEL':
            vels.append(float(line[2]))
        if hdr == 'HDG':
            hdgs.append(float(line[2]))
        if hdr == 'DPT':
            dpts.append(float(line[2]))
        if hdr == 'XXX':
            xxxs.append(float(line[2]))
        if hdr == 'POS':
            lats.append(float(line[2]))
            lons.append(float(line[3]))
            dats.append(datetime)
        if hdr == 'SSS':
            port = [float(x) for x in line[3:508]]
            stbd = [float(x) for x in line[509:]]
            psss.append(port)
            ssss.append(stbd)
    print(len(dats), len(lats), len(xxxs), len(dpts), len(hdgs))
    if len(xxxs) == len(dats):
        df = pd.DataFrame({'datetime':dats, 'lat':lats, 'lon':lons,
                           'hdg':hdgs, 'dpt':dpts, 'vel':vels, 'xxx':xxxs})
    else:
        print('did not find xxxs')
        df = pd.DataFrame({'datetime':dats, 'lat':lats, 'lon':lons,
                           'hdg':hdgs, 'dpt':dpts, 'vel':vels})

    return df, np.asarray(psss), np.asarray(ssss)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        read_csv(sys.argv[1])
