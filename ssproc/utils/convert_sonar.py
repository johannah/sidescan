#! /usr/bin/env python
from logdoc2csv import parse_bin
from glob import glob
import os, sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        from_dir = sys.argv[1]
        if os.path.exists(from_dir):
            for f in glob(os.path.join(from_dir, '*.logdoc')):
                csvf = f.replace('.logdoc', '.csv')
                os.system('~/mrl-code/mrss/scripts/logdoc2csv.py %s > %s' %(f, csvf))
                #parse_bin(f)
        else:
            print("ERROR: input dir %s does not exist" %from_dir)
