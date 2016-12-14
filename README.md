# Introduction
This is a small helper library for working with ecomapper sidescan data. The model for this sidescan is the StarFish 453 OEM. Check the examples directory for 
how to set up a config.py file for each project. Other scripts in the example 
directy will show how to plot and process various data points. 

# Data

## Ecomapper .log nav files contain data of the following types:
```
Index([u'datetime', u'latitude', u'longitude', u'number of sats',
       u'gps speed (kn)', u'gps true heading', u'gps magnetic variation',
       u'hdop', u'c magnetic heading', u'c true heading', u'pitch angle',
       u'roll angle', u'c inside temp (c)', u'dfs depth (m)',
       u'dtb height (m)', u'total water column (m)', u'batt percent',
       u'power watts', u'watt-hours', u'batt volts', u'batt ampers',
       u'batt state', u'time to empty', u'current step', u'dist to next (m)',
       u'next speed (kn)', u'vehicle speed (kn)', u'motor speed cmd',
       u'next heading', u'next long', u'next lat', u'next depth (m)',
       u'depth goal (m)', u'vehicle state', u'error state',
       u'distance to track (m)', u'fin pitch r', u'fin pitch l', u'pitch goal',
       u'fin yaw t', u'fin yaw b', u'yaw goal', u'fin roll', u'dvl-depth (m)',
       u'dvl -altitude (m)', u'dvl -water column (m)', u'dvl-fixtype',
       u'dvl-fixquality', u'dvl-temperature', u'conductivity (mmhos/cm)',
       u'temperature (c)', u'salinity (ppt)', u'sound speed (m/s)',
       u'date m/d/y   ', u'time hh:mm:ss', u'temp c', u'spcond ms/cm',
       u'sal ppt', u'depth feet', u'ph', u'ph mv', u'turbid+ ntu', u'chl ug/l',
       u'bga-pc cells/ml', u'odosat %', u'odo mg/l', u'battery volts',
       u'unnamed: 68', u'log_filename', u'vehicle speed (m/s)'],
      dtype='object')
```
## Ecomapper .log file data looks like:
```
                 datetime   latitude  longitude  number of sats  \
0 2016-01-11 16:23:25.340  13.191885 -59.640918               7
1 2016-01-11 16:23:26.340  13.191887 -59.640920               7
2 2016-01-11 16:23:27.360  13.191893 -59.640922               7
3 2016-01-11 16:23:28.360  13.191897 -59.640924               7
4 2016-01-11 16:23:29.360  13.191903 -59.640927               7

   gps speed (kn)  gps true heading  gps magnetic variation  hdop  \
0           1.041            318.87              -15.504097  1.80
1           0.854            321.29              -15.504097  1.80
2           0.550            321.29              -15.504097  1.80
3           0.834            321.29              -15.504097  1.79
4           1.431            333.24              -15.504097  1.79

   c magnetic heading  c true heading         ...           ph mv  \
0               330.7          316.57         ...           -75.2
1               335.7          321.62         ...           -75.2
2               344.6          330.65         ...           -75.3
3               344.9          330.95         ...           -75.4
4               341.4          327.40         ...           -75.5

   turbid+ ntu  chl ug/l  bga-pc cells/ml  odosat %  odo mg/l  battery volts  \
0          3.0      -2.1            -89.0     107.5      6.90           12.4
1          2.1      -2.4           -455.0     107.8      6.92           12.4
2          1.2      -0.4          -2201.0     108.1      6.96           12.2
3          3.5       1.1          -2281.0     108.3      6.94           12.4
4          3.5       0.9          -1158.0     108.5      6.96           12.4

   unnamed: 68                            log_filename  vehicle speed (m/s)
0          NaN  20160111_162318_Mission1_IVER2-218.log             0.000000
1          NaN  20160111_162318_Mission1_IVER2-218.log             0.000000
2          NaN  20160111_162318_Mission1_IVER2-218.log             0.437277
3          NaN  20160111_162318_Mission1_IVER2-218.log             0.447566
4          NaN  20160111_162318_Mission1_IVER2-218.log             0.519588

[5 rows x 70 columns]
```
# TODO



