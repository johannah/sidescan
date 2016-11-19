from ssproc.utils.io import load_ecomapper_logs
from ssproc.utils import plot
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
simg_name = 'data/bellairs.tif'
# UpperLeft and LowerRight Corners Lat Lon of the overview image
UL = (   13.1930568,  -59.6430313)
LR = (   13.1905824, -59.6396834)
df = load_ecomapper_logs('data/*BARBADOS*')
# pass in df to create contours
#gtiff, m = plot.create_geotiff(simg_name, UL, LR)


