from ssproc.utils.io import load_all_logs
from ssproc.utils import plot

simg_name = 'data/bellairs.tif'
# UpperLeft and LowerRight Corners Lat Lon of the overview image
UL = (   13.1930568,  -59.6430313)
LR = (   13.1905824, -59.6396834)
df = load_all_logs('data/*BARBADOS*.logdoc')
#gtiff, m = plot.create_contour_geotiff(simg_name, UL, LR, df=df)


