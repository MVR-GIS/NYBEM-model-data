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


def adh2raster(output_folder, adh_points, variable, barriers, mask):
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
    :param barriers:       line feature class; A line feature class
                           representing barriers used during interpolation.
    :param mask:           raster; A raster used to determine the
                           characteristics (dimensions, extent, cell size,
                           coordinate system, mask, snap) of the output raster.

    :return   A raster of the specified AdH variable interpolated across the
              extent of the mask raster.
    """
