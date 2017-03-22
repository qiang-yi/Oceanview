'''
Created on Mar 8, 2017

@author: Yi Qiang
'''

import arcpy
import time
import arcpy
import numpy
import math

arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")


arcpy.env.overwriteOutput=True

point_dir="D:/oceanview/obs_points/"
points_20k="D:/oceanview/other_data/sample_point_20k_2.shp"
dem_20k="D:/oceanview/LiDAR_dem/dsm_20k"
#dem_20k="D:/UH_work/oceanview/LiDAR_dem/dsm_20k"
output_dir="D:/oceanview/dist_obs_points/"
#output_dir="D:/UH_work/oceanview/viewshed_dsm/"
origin_dem="D:/oceanview/LiDAR_dem/dsm"
#origin_dem="D:/UH_work/oceanview/LiDAR_dem/dsm"

arcpy.env.extent =dem_20k
arcpy.env.snapRaster = dem_20k
#arcpy.env.mask = dem_20k

for row in arcpy.da.SearchCursor(points_20k, ["SHAPE@","FID"]):
    # Print x,y coordinates of each point feature

    fid=row[1]
    
    if fid >= 316 and fid<400:
        start_time=time.time()
        pt_file=point_dir+str(fid)+".shp"
        dist_file=output_dir+"dist_"+str(fid)
        outEucDistance = arcpy.sa.EucDistance(pt_file, "", dem_20k)
        outEucDistance=arcpy.sa.Int(outEucDistance)
        outEucDistance.save(dist_file)
        print("processing time for "+str(fid)+"th point is "+str(time.time()-start_time))
    
    