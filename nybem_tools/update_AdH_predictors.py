"""Calculate the AdH rasters for a scenario.

Calculates the AdH rasters for the required NYBEM variables into the
appropriate model subfolder. These raster predictors are required to calculate
the NYBEM ecological models.

:param: path_to_fwop:  string; Path to the parent folder of the existing
                       condition scenario (aka, Future WithOut Project, FWOP).
:param: path_to_alt:   string; Path to the parent folder of the alternative
                       in which the folder structure will be created.
:param: adh_velocity:  string; Path to the AdH folder holding the model
                       velocity results for this alternative.
:param: adh_salinity:  string; Path to the AdH folder holding the model
                       salinity results for this alternative.
:param: adh_wse:       string; Path to the AdH folder holding the model
                       water surface elevation results for this alternative.
:param: barriers:       line feature class; A line feature class
                       representing barriers used during interpolation.
:param: mask:           raster; A raster used to determine the
                       characteristics (dimensions, extent, cell size,
                       coordinate system, mask, snap) of the output raster.

:return:    None. AdH rasters for the specified alternative written to the
           appropriate subfolder for each model.
"""
import os
import arcpy
import utils
import importlib

# Ensure changes are reloaded during interactive development session
importlib.reload(arcpy)
importlib.reload(utils)

arcpy.env.compression = "LZW"


def main():

    arcpy.AddMessage("# ALT")  # -----------------------------------------------
    arcpy.AddMessage("## 10 Percentile Salinity")
    utils.adh2raster(output_folder=path_to_alt,
                     output_name="sal_10",
                     adh_points=adh_salinity,
                     variable="depth_avg1",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## MHHW")
    utils.adh2raster(output_folder=path_to_alt,
                     output_name="mhhw",
                     adh_points=adh_wse,
                     variable="MHHW",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## MLLW")
    utils.adh2raster(output_folder=path_to_alt,
                     output_name="mllw",
                     adh_points=adh_wse,
                     variable="MLLW",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## MTL")
    utils.adh2raster(output_folder=path_to_alt,
                     output_name="mtl",
                     adh_points=adh_wse,
                     variable="Mean_WSE",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)

    arcpy.AddMessage("# EST_INT")  # -------------------------------------------
    est_int_path = os.path.join(path_to_alt, "est_int", "predictors")

    arcpy.AddMessage("## Mean Salinity")
    utils.adh2raster(output_folder=est_int_path,
                     output_name="sal_mean_ann",
                     adh_points=adh_salinity,
                     variable="Mean_Depth",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## High Velocity")
    utils.adh2raster(output_folder=est_int_path,
                     output_name="vel_90",
                     adh_points=adh_velocity,
                     variable="vel_90",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## High Velocity, FWOP")
    fwop_est_int_path = os.path.join(path_to_fwop, "est_int", "predictors")
    arcpy.CopyRaster_management(os.path.join(fwop_est_int_path,
                                             "vel_90.tif"),
                                os.path.join(est_int_path,
                                             "fwop_vel_90.tif"))
    arcpy.AddMessage("## Edge Erosion")
    utils.rel_velocity(output_folder=est_int_path,
                       output_name="edge_erosion",
                       vel_alt=os.path.join(est_int_path,
                                            "vel_90.tif"),
                       vel_fwop=os.path.join(est_int_path,
                                             "fwop_vel_90.tif"))
    arcpy.AddMessage("## Depth Median")
    utils.adh2raster(output_folder=est_int_path,
                     output_name="wse_median",
                     adh_points=adh_wse,
                     variable="wse_50",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## Depth Maximum")
    utils.adh2raster(output_folder=est_int_path,
                     output_name="wse_100",
                     adh_points=adh_wse,
                     variable="wse_100",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## Episodic Sediment Deposition (aka Relative Depth)")
    utils.epi_sed_dep(output_folder=est_int_path,
                      output_name="esd",
                      wse_mhhw=os.path.join(path_to_alt, "mhhw.tif"),
                      wse_median=os.path.join(est_int_path, "wse_median.tif"),
                      wse_max=os.path.join(est_int_path, "wse_100.tif"))

    arcpy.AddMessage("# EST_SUB_HARD")  # --------------------------------------
    est_sub_hard_path = os.path.join(path_to_alt, "est_sub_hard", "predictors")

    arcpy.AddMessage("## Minimum Salinity")
    utils.adh2raster(output_folder=est_sub_hard_path,
                     output_name="sal_min_ann",
                     adh_points=adh_salinity,
                     variable="depth_avg_",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## Mean Salinity")
    utils.adh2raster(output_folder=est_sub_hard_path,
                     output_name="sal_mean_ann",
                     adh_points=adh_salinity,
                     variable="Mean_Depth",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)

    arcpy.AddMessage("# EST_SUB_SOFT_CLAM")  # ---------------------------------
    est_sub_soft_clam_path = os.path.join(path_to_alt, "est_sub_soft_clam",
                                          "predictors")

    arcpy.AddMessage("## Minimum Salinity")
    arcpy.CopyRaster_management(os.path.join(est_sub_hard_path,
                                             "sal_min_ann.tif"),
                                os.path.join(est_sub_soft_clam_path,
                                             "sal_min_ann.tif"))

    arcpy.AddMessage("# EST_SUB_SOFT_SAV")  # ----------------------------------
    est_sub_soft_sav_path = os.path.join(path_to_alt, "est_sub_soft_sav",
                                         "predictors")

    arcpy.AddMessage("## Depth Meters")
    utils.depth(output_folder=est_sub_soft_sav_path,
                output_name="depth",
                wse_mtl=os.path.join(path_to_alt, "mtl.tif"),
                bed_elevation=os.path.join(path_to_alt, "bed_elevation.tif"))
    arcpy.AddMessage("## Percent Light Available")
    utils.per_light_available(output_folder=est_sub_soft_sav_path,
                              output_name="pla",
                              depth_m=os.path.join(est_sub_soft_sav_path, 
                                                   "depth.tif"))
    
    arcpy.AddMessage("# FRESH_TID")  # -----------------------------------------
    fresh_tid_path = os.path.join(path_to_alt, "fresh_tid", "predictors")

    arcpy.AddMessage("## 10 Percent Salinity")
    arcpy.CopyRaster_management(os.path.join(path_to_alt, "sal_10.tif"),
                                os.path.join(fresh_tid_path, "sal_10.tif"))
    arcpy.AddMessage("## Episodic Sediment Deposition")
    utils.epi_sed_dep(output_folder=fresh_tid_path,
                      output_name="esd",
                      wse_mhhw=os.path.join(path_to_alt, "mhhw.tif"),
                      wse_median=os.path.join(est_int_path, "wse_median.tif"),
                      wse_max=os.path.join(est_int_path, "wse_100.tif"))

    arcpy.AddMessage("# MAR_DEEP")  # ------------------------------------------
    mar_deep_path = os.path.join(path_to_alt, "mar_deep", "predictors")

    arcpy.AddMessage("## Mean Salinity")
    arcpy.CopyRaster_management(os.path.join(est_sub_hard_path,
                                             "sal_mean_ann.tif"),
                                os.path.join(mar_deep_path,
                                             "sal_mean_ann.tif"))
    arcpy.AddMessage("## 10 Percentile Velocity")
    utils.adh2raster(output_folder=mar_deep_path,
                     output_name="vel_10",
                     adh_points=adh_velocity,
                     variable="vel_10",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## Low Velocity, FWOP")
    fwop_mar_deep_path = os.path.join(path_to_fwop, "mar_deep", "predictors")
    arcpy.CopyRaster_management(os.path.join(fwop_mar_deep_path,
                                             "vel_10.tif"),
                                os.path.join(mar_deep_path,
                                             "fwop_vel_10.tif"))
    arcpy.AddMessage("## Low Velocity Change")
    utils.rel_velocity(output_folder=est_int_path,
                       output_name="vel_change",
                       vel_alt=os.path.join(mar_deep_path,
                                            "vel_10.tif"),
                       vel_fwop=os.path.join(mar_deep_path,
                                             "fwop_vel_10.tif"))
    arcpy.AddMessage("## Percent Light Available")
    arcpy.CopyRaster_management(os.path.join(est_sub_soft_sav_path,
                                             "pla.tif"),
                                os.path.join(mar_deep_path,
                                             "pla.tif"))
    
    arcpy.AddMessage("# MAR_INT")  # -------------------------------------------
    mar_int_path = os.path.join(path_to_alt, "mar_int", "predictors")
    
    arcpy.AddMessage("## Minimum Depth")
    utils.adh2raster(output_folder=mar_int_path,
                     output_name="wse_0",
                     adh_points=adh_wse,
                     variable="wse_0",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## Exposure Duration (aka t_rel)")
    utils.expo_dur(output_folder=mar_int_path,
                   output_name="exp_dur",
                   wse_100=os.path.join(est_int_path, "wse_100.tif"),
                   wse_0=os.path.join(mar_int_path, "wse_0.tif"),
                   wse_mhhw=os.path.join(path_to_alt, "mhhw.tif"),
                   wse_mllw=os.path.join(path_to_alt, "mllw.tif"))

    arcpy.AddMessage("# MAR_SUB")  # -------------------------------------------
    mar_sub_path = os.path.join(path_to_alt, "mar_sub", "predictors")

    arcpy.AddMessage("## Median Velocity")
    utils.adh2raster(output_folder=mar_sub_path,
                     output_name="vel_50",
                     adh_points=adh_velocity,
                     variable="vel_50",
                     sql_select="",
                     barriers=barriers,
                     mask=mask)
    arcpy.AddMessage("## Percent Light Available")
    arcpy.CopyRaster_management(os.path.join(est_sub_soft_sav_path,
                                             "pla.tif"),
                                os.path.join(mar_sub_path,
                                             "pla.tif"))


if __name__ == "__main__":
    # Get input parameters
    path_to_fwop = arcpy.GetParameterAsText(0)
    path_to_alt = arcpy.GetParameterAsText(1)
    adh_velocity = arcpy.GetParameterAsText(2)
    adh_salinity = arcpy.GetParameterAsText(3)
    adh_wse = arcpy.GetParameterAsText(4)
    barriers = arcpy.GetParameterAsText(5)
    mask = arcpy.GetParameterAsText(6)

    main()
