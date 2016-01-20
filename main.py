# -*- coding: utf-8 -*-
"""
Wed Jan 20 2016

@author: Saxoriko, William Schuch
"""




# import modules
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import numpy as np

import os, sys

os.chdir("/home/user/git/PythonNDWI")

band4 = "/home/user/Downloads/pythonNDWI/LC81980242014260LGN00_sr_band4.tif"
band5 = "/home/user/Downloads/pythonNDWI/LC81980242014260LGN00_sr_band5.tif"

band4gdal = gdal.Open(band4, GA_ReadOnly)
band5gdal = gdal.Open(band5, GA_ReadOnly)

print "Driver: ", band4gdal.GetDriver().ShortName,"/", \
      band4gdal.GetDriver().LongName
print "Size is ",band4gdal.RasterXSize,"x",band4gdal.RasterYSize, \
      'x',band4gdal.RasterCount

print '\nProjection is: ', band4gdal.GetProjection()
print '\nProjection is: ', band5gdal.GetProjection()


print "\nInformation about the location of the image and the pixel size:"
geotransform = band4gdal.GetGeoTransform()
if not geotransform is None:
    print 'Origin = (',geotransform[0], ',',geotransform[3],')'
    print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'


band4Arr = band4gdal.ReadAsArray(0,0,band4gdal.RasterXSize, band4gdal.RasterYSize)
band5Arr = band5gdal.ReadAsArray(0,0,band5gdal.RasterXSize, band5gdal.RasterYSize)
print type(band4Arr)


# set the data type
band4Arr=band4Arr.astype(np.float32)
band5Arr=band5Arr.astype(np.float32)

# Derive the NDVI
mask = np.greater(band5Arr+band4Arr,0)

# set np.errstate to avoid warning of invalid values (i.e. NaN values) in the divide 

with np.errstate(invalid='ignore'):
    # NDWI = band 4 - band 5 / band 4 + band 5    
    ndwi = np.choose(mask,(-99,(band4Arr-band5Arr)/(band4Arr+band5Arr)))
print "NDWI min and max values", ndwi.min(), ndwi.max()
# Check the real minimum value
print ndwi[ndwi>-99].min()





# Write the result to disk
driver = gdal.GetDriverByName('GTiff')
if not os.path.exists("./data"):
    os.mkdir("./data")
outDataSet=driver.Create('./data/ndwi.tif', band4gdal.RasterXSize, band4gdal.RasterYSize, 1, GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(ndwi,0,0)
outBand.SetNoDataValue(-99)

# set the projection and extent information of the dataset
outDataSet.SetProjection(band4gdal.GetProjection())
outDataSet.SetGeoTransform(band4gdal.GetGeoTransform())


# Finally let's save it... or like in the OGR example flush it
outBand.FlushCache()
outDataSet.FlushCache()

# In shell
#cd /home/user/git/PythonNDWI
#chmod +x reproject.sh

import subprocess
subprocess.call(['./reproject.sh'])






