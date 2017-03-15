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

point_dir="C:/Users/Yi Qiang/Documents/UH_work/oceanview/obs_points/"
points_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/other_data/sample_point_20k.shp"
dem_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/other_data/dem_20k"
#dem_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm_20k"
output_dir="C:/Users/Yi Qiang/Documents/UH_work/oceanview/dist_obs_points/"
#output_dir="C:/Users/Yi Qiang/Documents/UH_work/oceanview/viewshed_dsm/"
origin_dem="C:/Users/Yi Qiang/Documents/UH_work/oceanview/Oahu_DEM_10m/dem_10m"
#origin_dem="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm"

arcpy.env.extent =dem_20k
arcpy.env.snapRaster = dem_20k
#arcpy.env.mask = dem_20k

for row in arcpy.da.SearchCursor(points_20k, ["SHAPE@","RASTERVALU","FID"]):
    # Print x,y coordinates of each point feature

    fid=row[2]
    
    if fid >= 83 and fid<84:
        start_time=time.time()
        pt_file=point_dir+str(fid)+".shp"
        dist_file=output_dir+"dist_"+str(fid)
        outEucDistance = arcpy.sa.EucDistance(pt_file, "", dem_20k)
        outEucDistance=arcpy.sa.Int(outEucDistance)
        outEucDistance.save(dist_file)
        print("processing time for "+str(fid)+"th point is "+str(time.time()-start_time))
    
    