#!/bin/bash
pwd
#gdalwarp -t_srs "EPSG:4326" ./data/ndwi.tif ./data/ndwi_ll.tif
gdaltransform -s_srs EPSG:32631 -t_srs EPSG:4326

# Let's check what the result is
gdalinfo ./data/ndwi_ll.tif