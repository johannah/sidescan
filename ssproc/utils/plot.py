import math
import os, sys
from datetime import datetime
from glob import glob
from datetime import timedelta
from copy import deepcopy
import numpy as np
import pandas as pd
import logging

from skimage.io import imread, imsave
from scipy.signal import medfilt, correlate2d

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import LatLon
import gdal
from osgeo import osr
from mpl_toolkits.basemap import Basemap, addcyclic
plt.style.use('ggplot')

import geotiff_meta_generator as gtmg
from mrss_tools import make_ordered_list
def create_basemap_object(UL, LR):
    """
    create a basemap object for plotting geospatial data - is fairly slow
    :UL: tuple of floats (lat,lon) Upper left coordinates from screenshot
    :LR tuple of floats (lat,lon) Upper left coordinates from screenshot
    returns basemap object with mercator projection"""
    m = Basemap(projection='merc', ellps='WGS84',
    llcrnrlat=LR[0],
    urcrnrlat=UL[0],
    llcrnrlon=UL[1],
    urcrnrlon=LR[1],
    resolution='h')
    return m

def create_geotiff(screenshot_name, UL, LR, m=None, df=None, contour_on='Total Water Column (m)'):
    """
    screenshot_name is name of image file, usually a screenshot from google maps
    :UL: tuple of floats (lat,lon) Upper left coordinates from screenshot
    :LR tuple of floats (lat,lon) Upper left coordinates from screenshot

    :m is basemap object, if none provided, it will be created with UL, LR
    :contours pass in a pandas dataframe with "Latitude, Longitude" and a data column to contour_on.
    :contour_on: The name of the float data column from df to build the contour on. By default this is "Total Water Column (m)"
    returns geotiff with filename of screenshot_name_geo.tif
    """
    if m is None:
        logging.info("Creating basemap object, this may take a while")
        m = create_basemap_object(UL, LR)
    # read provided image
    logging.info("Reading screenshot file %s" %screenshot_name)
    gtiff = imread(screenshot_name)
    # plot
    plt.figure(figsize=(8,8))
    m.imshow(gtiff[::-1,:])

    bname = '.'.join(screenshot_name.split('.')[:-1])
    # no contour
    if df is None:
        geotiff_name = bname + '_geo' + '.tif'
        meta_name =   bname + '.meta'
    else:
        # make contour_on filename that is safe
        geotiff_name = bname + '_%sgeo' %"".join(x for x in contour_on if x.isalnum()) + '.tif'
        meta_name =   bname + "".join(x for x in contour_on if x.isalnum()) + '.meta'

        yu, xu = m(np.asarray(lf['Longitude']),
                   np.asarray(lf['Latitude']))
        xi = np.linspace(max(xu), min(xu), gtiff.shape[1])
        yi = np.linspace(min(yu), max(yu), gtiff.shape[0])
        X, Y = np.meshgrid(xi, yi)

        z = lf[contour_on]
        zi = mlab.griddata(xu, yu, z, xi, yi, interp='linear')
        zif = gaussian_filter(zi, sigma=4)

        m.contourf(Y, X, zif, cmap=plt.cm.Blues, levels=np.linspace(z.min(), z.max(), 7))
        t = m.contour(Y, X, zif, colors='k', levels=np.linspace(z.min(), z.max(), 7))

        plt.clabel(t, fontsize=9, inline=1)
    plt.show()
    gtmg.save_geotiff_meta(UL, LR, gtiff.shape, meta_name)
    # needs gdal to run
    logging.info("Creating geotif image: %s" %geotiff_name)
    os.system('geotifcp -g %s %s %s' %(meta_name, screenshot_name, geotiff_name))
    return gtiff, m

def plot_contour(lf, m, gtiff=None, on="Total Water Column(m)", sigma=2):
    """
    :lf is pandas data file with Longitude, Latitude cols
    :m  is the basemap to plot data on
    :gtiff optional overhead image to plot tracks on.
    :on is column to plot color on, defaults to Total Water Column
    :sigma sigma value for gaussian filter on z values on map
    """
    yu, xu = m(np.asarray(lf['Longitude']),
               np.asarray(lf['Latitude']))
    xi = np.linspace(max(xu), min(xu), gtiff.shape[1])
    yi = np.linspace(min(yu), max(yu), gtiff.shape[0])
    X, Y = np.meshgrid(xi, yi)

    z = lf[on]
    zi = mlab.griddata(xu, yu, z, xi, yi, interp='linear')
    zif = gaussian_filter(zi, sigma=sigma)

    plt.figure(figsize=(10,8))
    if gtiff is not  None:
        m.imshow(gtiff[::-1, :])
    m.contourf(Y, X, zif, cmap=plt.cm.Blues, levels=np.linspace(z.min(), z.max(), 7))
    plt.colorbar()
    plt.legend()
    plt.show()

def plot_tracks(lf, m, gtiff=None, on="Total Water Column (m)"):
    """
    :lf is pandas data file with Longitude, Latitude cols
    :m  is the basemap to plot data on
    :gtiff optional overhead image to plot tracks on
    :on is column to plot color on, defaults to Total Water Column
    """

    yu, xu = m(np.asarray(lf['Longitude']),
               np.asarray(lf['Latitude']))
    plt.figure(figsize=(10,8))
    if gtiff is not  None:
        m.imshow(gtiff[::-1, :])
    m.scatter(yu, xu, c=lf[on], vmin=0, vmax=7, cmap=plt.cm.RdPu, edgecolor="None",  s=10)
    plt.colorbar()
    plt.legend()
    plt.show()

