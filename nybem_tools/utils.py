"""This module contains utility functions used throughout this package
"""


def copy_tif(from_path, to_path, name_pattern):
    """Copies files matching a pattern from one folder to another.

    :param from_path      Path to the folder where to original files reside.
    :param to_path        Path to the folder where the files will be copied.
    :param name_pattern   File name pattern to be matched.
    :return               None. Accomplishes side effect of copying files.
    """
    import glob
    import os
    import shutil
    import arcpy

    for file_ in glob.glob(os.path.join(from_path, name_pattern)):
        shutil.copy(file_, to_path)
    arcpy.AddMessage(name_pattern)


def adh2raster(output_folder, adh_points, variable, sql_select, barriers, mask):
    """Converts an AdH model point variable to a raster.

    AdH mesh nodes are often exported as points with an attribute table. This
    attribute table contains variables that have been calculated by AdH. These
    values must be interpolated to a raster for use in ecological models.

    :param output_folder:  string; Path to the output folder where the raster
                           will be written.
    :param adh_points:     point feature class; AdH mesh nodes output to a
                           point feature class.
    :param variable:       string; The name of the variable to be interpolated
                           to raster.
    :param sql_select:     string; An SQL SELECT statement applied to the
                           adh_points feature class.
    :param barriers:       line feature class; A line feature class
                           representing barriers used during interpolation.
    :param mask:           raster; A raster used to determine the
                           characteristics (dimensions, extent, cell size,
                           coordinate system, mask, snap) of the output raster.

    :return   None. Accomplishes the side effect of saving a raster to the
              output_folder of the specified AdH variable interpolated across
              the extent of the mask raster in .tif format.
    """
    import os
    import arcpy
    from timeit import default_timer as timer
    from datetime import timedelta

    arcpy.env.workspace = output_folder
    arcpy.env.scratchWorkspace = output_folder
    arcpy.env.outputCoordinateSystem = mask
    arcpy.env.extent = mask
    arcpy.env.cellSize = mask
    arcpy.env.snapRaster = mask
    # Do not set `arcpy.env.mask = mask`, it causes SplineWithBarriers fail.
    arcpy.env.compression = "LZW"
    arcpy.env.overwriteOutput = True

    arcpy.AddMessage(output_folder)
    arcpy.AddMessage(adh_points)
    arcpy.AddMessage(variable)
    arcpy.AddMessage(sql_select)
    arcpy.AddMessage(barriers)
    arcpy.AddMessage(mask)

    # Filter AdH points
    start = timer()
    arcpy.MakeFeatureLayer_management(adh_points, "filtered_points",
                                      sql_select)
    end = timer()
    arcpy.AddMessage(f"AdH points filtered. {timedelta(seconds=end - start)}")

    # Interpolate points to raster
    start = timer()
    interp_raster_name = str(variable) + "_nomask.tif"
    interp_raster_path = os.path.join(output_folder, interp_raster_name)
    cellsize = arcpy.GetRasterProperties_management(mask, 'CELLSIZEX')

    # Do not use `arcpy.sa.SplineWithBarriers()`; way too slow.
    arcpy.SplineWithBarriers_3d("filtered_points",
                                variable,
                                barriers,
                                cellsize.getOutput(0),
                                interp_raster_path, 0)
    end = timer()
    arcpy.AddMessage(f"Raster interpolated. {timedelta(seconds=end-start)}")

    # Remove nodata areas from interpolated raster
    start = timer()
    raster_masked = arcpy.sa.Times(interp_raster_path, mask)
    end = timer()
    arcpy.AddMessage(f"Raster masked. {timedelta(seconds=end - start)}")

    # Save output
    start = timer()
    output_raster_name = str(variable) + ".tif"
    output_raster_path = os.path.join(output_folder, output_raster_name)
    arcpy.CopyRaster_management(raster_masked, output_raster_path)
    end = timer()
    arcpy.AddMessage(f"Raster saved. {timedelta(seconds=end - start)}")

    # Cleanup
    arcpy.Delete_management(interp_raster_path)
