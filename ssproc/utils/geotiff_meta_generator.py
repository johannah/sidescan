import math

def sign(d):
  return 2*(d>0)-1

def format_latlon(nn):
  d = int(math.floor(nn))
  r = (nn-d)*60
  m = int(math.floor(r))
  s = (r-m)*60
  return "{d:>3d}d{m:02d}'{s:.2f}\"".format(d=d,m=m,s=s)

def format_lat_lon(lat,lon):
  s_lat = 'N' if sign(lat)>0 else 'S'
  s_lon = 'E' if sign(lon)>0 else 'W'
  return (format_latlon(abs(lat))+s_lat,format_latlon(abs(lon))+s_lon)

metastring = """Geotiff_Information:
   Version: 1
   Key_Revision: 1.0
   Tagged_Information:
      ModelTiepointTag (2,3):
         0                0                0
         {ul_lon:<15.9g}  {ul_lat:<15.9g}  0
      ModelPixelScaleTag (1,3):
         {scale_x:<15.9g}  {scale_y:<15.9g}  1
      End_Of_Tags.
   Keyed_Information:
      GTModelTypeGeoKey (Short,1): ModelTypeGeographic
      GTRasterTypeGeoKey (Short,1): RasterPixelIsArea
      GeographicTypeGeoKey (Short,1): GCS_WGS_84
      GeogAngularUnitsGeoKey (Short,1): Angular_Degree
      End_Of_Keys.
   End_Of_Geotiff.

GCS: 4326/WGS 84
Datum: 6326/World Geodetic System 1984
Ellipsoid: 7030/WGS 84 (6378137.00,6356752.31)
Prime Meridian: 8901/Greenwich (0.000000/  0d 0' 0.00"E)

Corner Coordinates:
Upper Left    ({ul_lon_s:>14s},{ul_lat_s:>14s})
Lower Left    ({ul_lon_s:>14s},{lr_lat_s:>14s})
Upper Right   ({lr_lon_s:>14s},{ul_lat_s:>14s})
Lower Right   ({lr_lon_s:>14s},{lr_lat_s:>14s})
Center        ({c_lon_s:>14s},{c_lat_s:>14s})
"""

'''
ul_lat = 33.44562
ul_lon = -118.48670
lr_lat = 33.44345
lr_lon = -118.48289
px_x = 1420
px_y = 969
'''
'''
# Long-Wharf1.jpg
ul_lat =  34.036145
ul_lon = -118.539438
lr_lat =  34.031332
lr_lon = -118.531541
px_x = 1388
px_y = 1002

# Long-Wharf-BayWatch.jpg
ul_lat =  34.032865
ul_lon = -118.533725
lr_lat =  34.027746
lr_lon = -118.525330
px_x = 1388
px_y = 1002


# Sunset.jpg
ul_lat =  34.039428
ul_lon = -118.561378
lr_lat =  34.035230
lr_lon = -118.55449
px_x = 1388
px_y = 1002
'''


def generate_geotiff_meta(ul_coords,lr_coords,im_size):

  ul_lat = ul_coords[0]
  ul_lon = ul_coords[1]

  lr_lat = lr_coords[0]
  lr_lon = lr_coords[1]

  px_x = im_size[0]
  px_y = im_size[1]

  (ul_lat_s,ul_lon_s) = format_lat_lon(ul_lat,ul_lon)
  (lr_lat_s,lr_lon_s) = format_lat_lon(lr_lat,lr_lon)

  scale_x = abs(ul_lon-lr_lon)/px_x
  scale_y = abs(ul_lat-lr_lat)/px_y

  c_lon = (ul_lon+lr_lon)/2
  c_lat = (ul_lat+lr_lat)/2

  (c_lat_s,c_lon_s) = format_lat_lon(c_lat,c_lon)

  vars = {'ul_lat_s':ul_lat_s,'ul_lon_s':ul_lon_s,'lr_lat_s':lr_lat_s,'lr_lon_s':lr_lon_s,'scale_x':scale_x,'scale_y':scale_y,'c_lon_s':c_lon_s,'c_lat_s':c_lat_s,'ul_lon':ul_lon,'ul_lat':ul_lat}

  return metastring.format(**vars)

def save_geotiff_meta(ul_coords,lr_coords,im_size,filename):
  res = generate_geotiff_meta(ul_coords,lr_coords,im_size)
  print(res)
  f = open(filename,'w')
  f.write(res)
  f.close()

