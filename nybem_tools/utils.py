"""This module contains utility functions used throughout this package
"""


def copy_tif(from_path, to_path, name_pattern):
    """Copies files matching a pattern from one folder to another.

    :param: from_path      Path to the folder where to original files reside.
    :param: to_path        Path to the folder where the files will be copied.
    :param: name_pattern   File name pattern to be matched.

    :return:  None. Accomplishes side effect of copying files.
    """
    import glob
    import os
    import shutil
    import arcpy

    for file_ in glob.glob(os.path.join(from_path, name_pattern)):
        shutil.copy(file_, to_path)
    arcpy.AddMessage(name_pattern)


def adh2raster(output_folder, output_name, adh_points, variable, sql_select,
               barriers, mask):
    """Converts an AdH model point variable to a raster.

    AdH mesh nodes are often exported as points with an attribute table. This
    attribute table contains variables that have been calculated by AdH. These
    values must be interpolated to a raster for use in ecological models.

    :param: output_folder: string; Path to the output folder where the raster
                           will be written.
    :param: output_name:   string; Name of the output raster.
    :param: adh_points:    point feature class; AdH mesh nodes output to a
                           point feature class.
    :param: variable:      string; The name of the variable to be interpolated
                           to raster.
    :param: sql_select:    string; An SQL SELECT statement applied to the
                           adh_points feature class.
    :param: barriers:      line feature class; A line feature class
                           representing barriers used during interpolation.
    :param: mask:          raster; A raster used to determine the
                           characteristics (dimensions, extent, cell size,
                           coordinate system, mask, snap) of the output raster.

    :return:  None. Accomplishes the side effect of saving a raster to the
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

    # arcpy.AddMessage(output_folder)
    arcpy.AddMessage(os.path.basename(adh_points))
    arcpy.AddMessage(variable)
    # arcpy.AddMessage(sql_select)
    # arcpy.AddMessage(barriers)
    # arcpy.AddMessage(mask)

    # Filter AdH points
    start = timer()
    arcpy.MakeFeatureLayer_management(adh_points, "filtered_points",
                                      sql_select)
    end = timer()
    arcpy.AddMessage(f"AdH points filtered. {timedelta(seconds=end - start)}")

    # Interpolate points to raster
    start = timer()
    interp_raster_name = str(output_name) + "_nomask.tif"
    interp_raster_path = os.path.join(output_folder, interp_raster_name)
    cellsize = arcpy.GetRasterProperties_management(mask, "CELLSIZEX")

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
    output_raster_name = str(output_name) + ".tif"
    output_raster_path = os.path.join(output_folder, output_raster_name)
    arcpy.CopyRaster_management(raster_masked, output_raster_path)
    end = timer()
    arcpy.AddMessage(f"Raster saved. {timedelta(seconds=end - start)}")

    # Cleanup
    arcpy.Delete_management(interp_raster_path)


def edge_erosion(output_folder, output_name, vel_alt, vel_fwop):
    """Calculates an Edge Erosion Raster.

    Edge Erosion is based on the concept of relative current velocity.
    Relative current velocity can be operationalized as the percent increase
    in velocity from the baseline condition.

    PercentIncrease = ((value_new − value_original) / value_original) ∗ 100

    :param: output_folder: string; Path to the output folder where the raster
                           will be written.
    :param: output_name:   string; Name of the output raster.
    :param: vel_alt:       raster; The velocity for the alternative being
                           evaulated.
    :param: vel_fwop:      raster; The velocity for the baseline condition.

    :return:  None. Accomplishes the side effect of saving a raster to the
              output_folder of the calculated percent increase in the velocity
              from the baseline condition in .tif format.
    """
    import os
    import arcpy
    from arcpy.sa import Raster
    from timeit import default_timer as timer
    from datetime import timedelta

    arcpy.env.compression = "LZW"
    arcpy.env.overwriteOutput = True

    arcpy.AddMessage(vel_alt)
    arcpy.AddMessage(vel_fwop)

    start = timer()
    edge_eros = ((Raster(vel_alt) - Raster(vel_fwop)) / Raster(vel_fwop)) * 100
    end = timer()
    arcpy.AddMessage(f"Calculated raster. {timedelta(seconds=end - start)}")

    # Save output
    start = timer()
    output_raster_name = str(output_name) + ".tif"
    output_raster_path = os.path.join(output_folder, output_raster_name)
    arcpy.CopyRaster_management(edge_eros, output_raster_path)
    end = timer()
    arcpy.AddMessage(f"Raster saved. {timedelta(seconds=end - start)}")


def epi_sed_dep(output_folder, output_name, wse_mhhw, wse_median, wse_max):
    """Calculate Episodic Sediment Deposition.

    Episodic Sediment Deposition is calculated using the following formula:

    ESD = (Depth_MHHW − Depth_median) / (Depth_max − Depth_median)

    :param: output_folder: string; Path to the output folder where the raster
                           will be written.
    :param: output_name:   string; Name of the output raster.
    :param: wse_mhhw:      raster; The mean higher high water (WHHW) water
                           surface elevation.
    :param: wse_median:    raster; The median water surface elevation.
    :param: wse_max:       raster; The maximum water surface elevation.

    :return:  None. Accomplishes the side effect of saving a raster to the
              output_folder of the calculated percent increase in the velocity
              from the baseline condition in .tif format.
    """
    import os
    import arcpy
    from arcpy.sa import Raster
    from timeit import default_timer as timer
    from datetime import timedelta

    arcpy.env.compression = "LZW"
    arcpy.env.overwriteOutput = True

    arcpy.AddMessage(wse_mhhw)
    arcpy.AddMessage(wse_median)
    arcpy.AddMessage(wse_max)

    start = timer()
    esd = (Raster(wse_mhhw) - Raster(wse_median)) / (Raster(wse_max) -
                                                     Raster(wse_median))
    end = timer()
    arcpy.AddMessage(f"Calculated raster. {timedelta(seconds=end - start)}")

    # Save output
    start = timer()
    output_raster_name = str(output_name) + ".tif"
    output_raster_path = os.path.join(output_folder, output_raster_name)
    arcpy.CopyRaster_management(esd, output_raster_path)
    end = timer()
    arcpy.AddMessage(f"Raster saved. {timedelta(seconds=end - start)}")


def depth(output_folder, output_name, wse_mtl, bed_elevation):
    """Calculate Depth at Mean Water Surface Elevation.

    Calculates depth of water at the mean water surface elevation using the
    following formula:

    depth = water_surface_mean - bed_elevation

    :param: output_folder: string; Path to the output folder where the raster
                           will be written.
    :param: output_name:   string; Name of the output raster.
    :param: wse_mtl:       raster; The mean water surface elevation.
    :param: bed_elevation: raster; The bed elevation elevation raster.

    :return:  None. Accomplishes the side effect of saving a raster to the
              output_folder of the calculated mean water depth in .tif format.
    """
    import os
    import arcpy
    from arcpy.sa import Raster
    from timeit import default_timer as timer
    from datetime import timedelta

    arcpy.env.compression = "LZW"
    arcpy.env.overwriteOutput = True

    arcpy.AddMessage(wse_mtl)
    arcpy.AddMessage(bed_elevation)

    start = timer()
    depth_m = Raster(wse_mtl) - Raster(bed_elevation)
    end = timer()
    arcpy.AddMessage(f"Calculated raster. {timedelta(seconds=end - start)}")

    # Save output
    start = timer()
    output_raster_name = str(output_name) + ".tif"
    output_raster_path = os.path.join(output_folder, output_raster_name)
    arcpy.CopyRaster_management(depth_m, output_raster_path)
    end = timer()
    arcpy.AddMessage(f"Raster saved. {timedelta(seconds=end - start)}")


def per_light_available(output_folder, output_name, depth_m):
    """Calculates the Percent Light Available.

    Calculates the percent of light available at a given depth using the
    following formula:

    PLA = exp(−1.39 ∗ depth) ∗ 100

    :param: output_folder: string; Path to the output folder where the raster
                           will be written.
    :param: output_name:   string; Name of the output raster.
    :param: depth:         raster; The depth raster.

    :return:  None. Accomplishes the side effect of saving a raster to the
              output_folder of the calculated percent light available in
              .tif format.
    """
    import os
    import arcpy
    from arcpy.sa import Raster
    from timeit import default_timer as timer
    from datetime import timedelta

    arcpy.env.compression = "LZW"
    arcpy.env.overwriteOutput = True

    arcpy.AddMessage(depth_m)

    start = timer()
    pla = arcpy.sa.Exp(-1.39 * Raster(depth_m)) * 100
    end = timer()
    arcpy.AddMessage(f"Calculated raster. {timedelta(seconds=end - start)}")

    # Save output
    start = timer()
    output_raster_name = str(output_name) + ".tif"
    output_raster_path = os.path.join(output_folder, output_raster_name)
    arcpy.CopyRaster_management(pla, output_raster_path)
    end = timer()
    arcpy.AddMessage(f"Raster saved. {timedelta(seconds=end - start)}")


def expo_dur(output_folder, output_name, wse_100, wse_0, wse_mhhw,
                      wse_mllw):
    """Calculate Exposure Duration.
    Calculate the exposure duration using the following equation:

    t_rel = (H_max − H_min) / (MHHW − MLLW)

    :param: output_folder: string; Path to the output folder where the raster
                           will be written.
    :param: output_name:   string; Name of the output raster.
    :param: wse_100:       raster; The maximum water surface elevation.
    :param: wse_0:         raster; The minimum water surface elevation.
    :param: wse_mhhw:      raster; The mean higher high water (WHHW) water
                           surface elevation.
    :param: wse_mllw:      raster; The mean lower low water (WLLW) water
                           surface elevation.

    :return:  None. Accomplishes the side effect of saving a raster to the
              output_folder of the calculated exposure duration in .tif format.
    """
    import os
    import arcpy
    from arcpy.sa import Raster
    from timeit import default_timer as timer
    from datetime import timedelta

    arcpy.env.compression = "LZW"
    arcpy.env.overwriteOutput = True

    arcpy.AddMessage(wse_100)
    arcpy.AddMessage(wse_0)
    arcpy.AddMessage(wse_mhhw)
    arcpy.AddMessage(wse_mllw)

    start = timer()
    exposure_duration = (Raster(wse_100) - Raster(wse_0)) / (Raster(wse_mhhw) -
                                                             Raster(wse_mllw))
    end = timer()
    arcpy.AddMessage(f"Calculated raster. {timedelta(seconds=end - start)}")

    # Save output
    start = timer()
    output_raster_name = str(output_name) + ".tif"
    output_raster_path = os.path.join(output_folder, output_raster_name)
    arcpy.CopyRaster_management(exposure_duration, output_raster_path)
    end = timer()
    arcpy.AddMessage(f"Raster saved. {timedelta(seconds=end - start)}")
