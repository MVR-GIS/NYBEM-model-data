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
:param sql_select      string; An SQL SELECT statement applied to the
                       adh_points feature class.
:param barriers:       line feature class; A line feature class
                       representing barriers used during interpolation.
:param mask:           raster; A raster used to determine the
                       characteristics (dimensions, extent, cell size,
                       coordinate system, mask, snap) of the output raster.

:return   A raster of the specified AdH variable interpolated across the
          extent of the mask raster.
"""
import arcpy
import utils
import importlib

# Ensure changes are reloaded during interactive development
importlib.reload(arcpy)
importlib.reload(utils)

def main():
    utils.adh2raster(output_folder, adh_points, variable, sql_select,
                     barriers, mask)


if __name__ == "__main__":
    # Get input parameters
    output_folder = arcpy.GetParameterAsText(0)
    adh_points = arcpy.GetParameterAsText(1)
    variable = arcpy.GetParameterAsText(2)
    sql_select = arcpy.GetParameterAsText(3)
    barriers = arcpy.GetParameterAsText(4)
    mask = arcpy.GetParameterAsText(5)

    main()
