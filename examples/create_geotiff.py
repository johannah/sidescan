from ssproc.utils import plot

simg_name = 'data/bellairs.tif'
# UpperLeft and LowerRight Corners Lat Lon of the overview image
UL = (   13.1930568,  -59.6430313)
LR = (   13.1905824, -59.6396834)
gtiff, m = plot.create_geotiff(simg_name, UL, LR)


