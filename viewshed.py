'''
Created on Feb 25, 2017

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
points_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/other_data/sample_point_20k_2.shp"
dem_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm_20k_int"
#dem_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm_20k"
output_dir="C:/Users/Yi Qiang/Documents/UH_work/oceanview/viewshed_dsm/"
output_dist_dir="C:/Users/Yi Qiang/Documents/UH_work/oceanview/dist_obs_points/"
#output_dir="C:/Users/Yi Qiang/Documents/UH_work/oceanview/viewshed_dsm/"
origin_dem="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm_20k_int"
#origin_dem="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm"

arcpy.env.extent =dem_20k
arcpy.env.snapRaster = dem_20k
#arcpy.env.mask = dem_20k

for row in arcpy.da.SearchCursor(points_20k, ["SHAPE@","FID"]):
    # Print x,y coordinates of each point feature
    #
    pnt_obj=row[0]
    #dist=row[1]
    fid=row[1]
    
    if fid >= 94 and fid<100:
        start_time = time.time()
        fname=str(fid)+'.shp'
        pnt=arcpy.CreateFeatureclass_management(point_dir, fname, "POINT", "C:/Users/Yi Qiang/Documents/UH_work/oceanview/other_data/sea_point.shp", "", "", origin_dem)
        arcpy.AddField_management(pnt, "Dist_Coast", "FLOAT")
        cursor = arcpy.da.InsertCursor(pnt, ["SHAPE@"])
        cursor.insertRow([pnt_obj])
        
        viewshed_output=output_dir+"view"+str(fid)
        arcpy.Viewshed_3d(dem_20k, pnt, viewshed_output, "", "CURVED_EARTH")
        
        
        #arcpy.Delete_management(output_dir+"view"+str(fid))

        print "processing time for "+str(fid)+"th point is "+ str(time.time()-start_time)
