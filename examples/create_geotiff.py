from ssproc.utility.plot_spatial import create_geotiff
import config as cc
import os
create_geotiff(cc.map_image_path, cc.geotiff_path, cc.UL_map_image, cc.LR_map_image)


