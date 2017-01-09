import math
import os, sys
from datetime import datetime
from glob import glob
from datetime import timedelta
from copy import deepcopy
import numpy as np
import pandas as pd
import logging

from scipy.misc import imread, imsave

#from extract_sonar_csv import read_csv
import matplotlib.pyplot as plt
#from logdoc2csv import parse_bin

def make_ordered_list(cvs):
    """This function will sort WP sidescan files
    into an ordered list by waypoints
    """
    cvns = ['']*(1000)
    max_val = 2
    for path in cvs:
        i = os.path.split(path)[1]
        index_i = int(i[i.index("WP")+2:].replace(".csv", ""))-1
        #print(index_i, len(cvns), max_val)
        cvns[index_i] = path
        if index_i > max_val:
            max_val = index_i
    return cvns[:max_val+1]

def load_sidescan_logs(path):
    """
    :path path, glob search, or a directory from which to load all files into pandas dataframe
    filetype can be '.csv' or '.logdoc'. If .logdoc, the file is first converted
    csv and then read
    """
    # if the path is a directory
    if os.path.isdir(path):
        lfiles = glob(os.path.join(path))
    # else put this log file name in a list
    elif os.path.exists(path):
        lfiles = [path]
    else:
        lfiles = glob(path)

    if not len(lfiles):
        logging.error("Could not find any log data files at: %s" %path)

    csv_files = []
    for ff in lfiles:
        bname = '.'.join(ff.split('.')[:-1])
        ftype = ff.split('.')[-1]
        csv_name = bname + '.csv'
        if ftype == 'csv':
            csv_files.append(ff)
        elif ftype == 'logdoc':
            # if there is not already a csv in our path
            if csv_name not in lfiles:
                # convert to csv file
                parse_bin(ff, csv_name)
                csv_files.append(csv_name)


    #for x, l in enumerate(csv_files):
    for x, l in enumerate(csv_files):
        logging.info("Reading %s into dataframe" %l)
        lf = pd.read_csv(l, sep=';', index_col=None, header=0,
              parse_dates={'datetime':[2,3]})#, ignore_index=True)
        #if x:
        #    la = os.path.split(l)[1]

        #    lf = lf.append(pd.read_csv(l, sep=';')#, index_col=None, header=0, parse_dates={'datetime':[2,3]}), ignore_index=True)
        #else:
        #    lf = pd.read_csv(l, sep=';', index_col=None, header=0, parse_dates={'datetime':[2,3]})

    #lf['Vehicle Speed (m/s)']  = lf['Vehicle Speed (kn)']*0.514444
    return lf


    for x, l in enumerate(csv_files):
        logging.info("Reading %s into dataframe" %l)
        # may fail if the csv file is not formatted correctly
        #if x:
        #    la = os.path.split(l)[1]
        #    lf = lf.append(l, sep=';', index_col=None, header=0,
        #                   parse_dates={'datetime':[2,3]},
        #                  ignore_index=True)
        ## initialize pandas
        #else:
        #    lf = pd.read_csv(l, sep=';', index_col=None, header=0,
        #                 parse_dates={'datetime':[2,3]})
    ## create m/s
    #lf['Vehicle Speed (m/s)']  = lf['Vehicle Speed (kn)']*0.514444
    #return lf

def load_ecomapper_log_files(path):
     # if the path is a directory
    if os.path.isdir(path):
        lfiles = glob(os.path.join(path,  '*.log'))
    # else put this log file name in a list
    elif os.path.exists(path):
        if path.endswith('.log'):
            lfiles = [path]
    else:
        # already has search char
        if '*' in path:
            lfiles = glob(path)
        else:
            lfiles = glob(os.path.join(path, '*.log'))

    if not len(lfiles):
        logging.error("Could not find any log data files at: %s" %path)


    for x, l in enumerate(lfiles):
        logging.info("Reading %s into dataframe" %l)
        # may fail if the csv file is not formatted correctly
        la = os.path.split(l)[1]
        if x:
            this_log = pd.read_csv(l, sep=';', index_col=None,
                                       header=0, parse_dates={'datetime':[2,3]})
            this_log['log_filename'] = la
            lf = lf.append(this_log, ignore_index=True)
        # initialize pandas
        else:
            lf = pd.read_csv(l, sep=';', index_col=None, header=0,
                             parse_dates={'datetime':[2,3]})
            lf['log_filename'] = la
    ## create m/s
    lf['Vehicle Speed (m/s)']  = lf['Vehicle Speed (kn)']*0.514444
    lf.rename(columns=lambda x: x.lower(), inplace=True)

    return lf

