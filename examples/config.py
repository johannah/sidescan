import pickle
import time
import os
import sys
from scipy.misc import imread
from ssproc.utility.plot_spatial import create_basemap_object, create_geotiff, plot_tracks
from ssproc.utility.handle_files import load_ecomapper_log_files
"""
Use this file to set defaults for processing ecomapper data

"""


"""
DATA AND FILE HANDLING

"""

"""
CHANGE every project
"""
# string to use as base name for files
proj_name = 'bellairs'
# name of an overhead image of the area. this is used to create a geotif of the
# survey area for overlaying data and using vectormap. usually, we grab a
# screenshot of the area from google maps and note the upper left corner and
# lower left corner coordinates as degrees.
# relative path to overview tiff
map_image_path = 'data/bellairs.tif'
# upper left coordinates in degrees
# for small image
#UL_map_image =  (13.193114, -59.643621)
# for wide img
UL_map_image = (13.192721, -59.652515)
# lower right coordinates in degrees
LR_map_image = (13.187486, -59.638144)



################################################################################
"""
Rarely CHANGE
"""
# directory where subdirectories of data types are located
data_base_dir = 'data'

# directory where ecomapper sidescan files are stored. if file is binary.logdoc,
# .ss will be automatically created and used
sidescan_dir = 'ss'
# directory where ecomapper navigation files are stored.
nav_dir = 'nav'
fig_dir = 'figs'
basemap_name =  '%s_basemap.pkl' %proj_name
# TODO maybe write timestamp name

nav_df_name = "%s_df.pkl" %proj_name
tracks_name = "%s_tracks.tif" %proj_name

nav_path = os.path.join(data_base_dir, nav_dir)
ss_path = os.path.join(data_base_dir, sidescan_dir)
fig_path = os.path.join(data_base_dir, fig_dir)
# create necessary dirs
dirs = [data_base_dir, nav_path, ss_path, fig_dir]
for d in dirs:
    if not os.path.isdir(d):
        os.mkdir(d)

nav_df_path = os.path.join(nav_path, nav_df_name)
basemap_path = os.path.join(fig_path, basemap_name)
tracks_path = os.path.join(fig_path, tracks_name)

map_image_base = os.path.split(map_image_path)[1]
# remove file ending
bmap_image_base = '.'.join(map_image_base.split('.')[:-1])
geotiff_path = os.path.join(fig_path, bmap_image_base + '_geo.tif')
geotiff_contour_path = os.path.join(fig_path, bmap_image_base + '_contour_geo.tif')

def create_default_files(replace=False):
    if not replace:
        if not os.path.exists(basemap_path):
            m = create_basemap_object(UL_map_image, LR_map_image)
            pickle.dump(m, open(basemap_path, 'wb'))
        else:
            m = pickle.load(open(basemap_path, 'rb'))
        if not os.path.exists(geotiff_path):
            create_geotiff(map_image_path, geotiff_path, UL_map_image, LR_map_image)
        if not os.path.exists(nav_df_path):
            lf = load_ecomapper_log_files(nav_path)
            pickle.dump(lf, open(nav_df_path, 'wb'))
        else:
            lf = pickle.load(open(nav_df_path, 'rb'))
            if not os.path.exists(tracks_path):
                gtiff = imread(map_image_path)
                plot_tracks(lf, m, gtiff, tracks_path)
        #if not os.path.exists(geotiff_contour_path):
        #    contour_on = 'total water column (m)'
        #    create_geotiff(map_image_path, geotiff_contour_path,
        #                   UL_map_image, LR_map_image, m, lf, contour_on)
    else:
        m = create_basemap_object(UL_map_image, LR_map_image)
        pickle.dump(m, open(basemap_path, 'wb'))
        create_geotiff(map_image_path, geotiff_path, UL_map_image, LR_map_image)
        lf = load_ecomapper_log_files(nav_path)
        pickle.dump(lf, open(nav_df_path, 'wb'))
        gtiff = imread(map_image_path)
        plot_tracks(lf, m, gtiff, tracks_path)
    #if not os.path.exists(geotiff_contour_path):
    #    contour_on = 'total water column (m)'

if __name__ == "__main__":
    if len(sys.argv) == 2:
        replace = True
    else:
        replace = False
    create_default_files(replace)
