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
points_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/other_data/sample_point_20k.shp"
#dem_20k="C:/Users/Yi Qiang/Documents/UH_work/other_data/dem_20k"
dem_20k="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm_20k"
#output_dir="C:/Users/Yi Qiang/Documents/UH_work/viewshed4/"
output_dir="C:/Users/Yi Qiang/Documents/UH_work/oceanview/viewshed_dsm/"
#origin_dem="C:/Users/Yi Qiang/Documents/UH_work/Oahu_DEM/dem_10m"
origin_dem="C:/Users/Yi Qiang/Documents/UH_work/oceanview/LiDAR_dem/dsm"

arcpy.env.extent =dem_20k
arcpy.env.snapRaster = origin_dem
arcpy.env.mask = dem_20k

for row in arcpy.da.SearchCursor(points_20k, ["SHAPE@","RASTERVALU","FID"]):
    # Print x,y coordinates of each point feature
    #
    pnt_obj=row[0]
    dist=row[1]
    fid=row[2]
    
    if fid >= 0 and fid<50:
        start_time = time.time()
        fname=str(fid)+'.shp'
        pnt=arcpy.CreateFeatureclass_management(point_dir, fname, "POINT", "C:/Users/Yi Qiang/Documents/UH_work/oceanview/other_data/sea_point.shp", "", "", origin_dem)
        arcpy.AddField_management(pnt, "Dist_Coast", "FLOAT")
        cursor = arcpy.da.InsertCursor(pnt, ["SHAPE@","Dist_Coast"])
        cursor.insertRow([pnt_obj,dist])
        
        viewshed_output=output_dir+"view"+str(fid)
        arcpy.Viewshed_3d(dem_20k, pnt, viewshed_output, "", "CURVED_EARTH")
        #weight=int((50-dist/1000) / 50*100)
        #weight=int((1.55138827-numpy.arctan(dist/1200))/1.55138827*100)
        dist=dist/1000
        dxdy=1/(1+(dist/1.2)**2)
        dxdy_min=1/(1+(123/1.2)**2)
        dxdy_max=1/(1+(0/1.2)**2)
        weight=int((dxdy-dxdy_min)*1000/(dxdy_max-dxdy_min))
        print "dxdy:" +str(dxdy)
        print "dxdy_max:" +str(dxdy_max)
        print "dxdy_min:" +str(dxdy_min)
        print "dist: "+str(dist)
        print "weight: "+str(weight)

        viewshed=arcpy.Raster(viewshed_output) * weight
        print "start to save"+str(fid)+" th point"
        viewshed.save(output_dir+"w_view"+str(fid))
        #arcpy.Delete_management(output_dir+"view"+str(fid))

        print "processing time for "+str(fid)+"th point is "+ str(time.time()-start_time)
