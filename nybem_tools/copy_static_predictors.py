"""Copy static predictor variables from the existing condition scenario to
another scenario.

Some ecological modeling predictor variables are not varied during scenarios.
This tool copies the NYBEM ecological model variables that do not change from
the existing condition scenario into the folder structure of a new scenario.

:param: path_to_fwop:    string; Path to the parent folder of the existing
                         condition scenario (aka, future without project, FWOP).
:param: path_to_alt:     string; Path to the parent folder of the alternative
                         in which the folder structure will be created.

:return:    Static rasters copied from the existing condition scenario to the
            alternative folder.
"""
import os
import arcpy
from utils import copy_tif


def main():
    # alt root -----------------------------------------------------------------
    arcpy.AddMessage("# ALT")
    copy_tif(path_to_fwop, path_to_alt, "bed_elevation*")
    copy_tif(path_to_fwop, path_to_alt, "mask*")

    # est_int ------------------------------------------------------------------
    arcpy.AddMessage("# EST_INT")
    from_est_int = os.path.join(path_to_fwop, "est_int", "predictors")
    to_est_int = os.path.join(path_to_alt, "est_int", "predictors")

    copy_tif(from_est_int, to_est_int, "dev_100_per*")
    copy_tif(from_est_int, to_est_int, "shoreline_armoring*")
    copy_tif(from_est_int, to_est_int, "veg_50_per*")

    # est_sub_hard -------------------------------------------------------------
    arcpy.AddMessage("# EST_SUB_HARD")
    from_est_sub_hard = os.path.join(path_to_fwop, "est_sub_hard", "predictors")
    to_est_sub_hard = os.path.join(path_to_alt, "est_sub_hard", "predictors")

    copy_tif(from_est_sub_hard, to_est_sub_hard, "cultch*")
    copy_tif(from_est_sub_hard, to_est_sub_hard, "pct_gravel*")
    copy_tif(from_est_sub_hard, to_est_sub_hard, "est_sub_hard*")

    # est_sub_soft_clam --------------------------------------------------------
    arcpy.AddMessage("# EST_SUB_SOFT_CLAM")
    from_est_sub_soft_clam = os.path.join(path_to_fwop, "est_sub_soft_clam", "predictors")
    to_est_sub_soft_clam = os.path.join(path_to_alt, "est_sub_soft_clam", "predictors")

    copy_tif(from_est_sub_soft_clam, to_est_sub_soft_clam, "pct_sand*")
    # trailing dot needed to include multiple files!
    copy_tif(from_est_sub_soft_clam, to_est_sub_soft_clam, "est_sub_soft.*")

    # est_sub_soft_sav ---------------------------------------------------------
    arcpy.AddMessage("# EST_SUB_SOFT_SAV")
    from_est_sub_soft_sav = os.path.join(path_to_fwop, "est_sub_soft_sav", "predictors")
    to_est_sub_soft_sav = os.path.join(path_to_alt, "est_sub_soft_sav", "predictors")

    copy_tif(from_est_sub_soft_sav, to_est_sub_soft_sav, "est_sub_soft*")
    copy_tif(from_est_sub_soft_sav, to_est_sub_soft_sav, "pct_fines*")
    copy_tif(from_est_sub_soft_sav, to_est_sub_soft_sav, "vessel_density*")

    # fresh_tid ----------------------------------------------------------------
    arcpy.AddMessage("# FRESH_TID")
    from_fresh_tid = os.path.join(path_to_fwop, "fresh_tid", "predictors")
    to_fresh_tid = os.path.join(path_to_alt, "fresh_tid", "predictors")

    copy_tif(from_fresh_tid, to_fresh_tid, "veg_50_per*")

    # mar_deep -----------------------------------------------------------------
    arcpy.AddMessage("# MAR_DEEP")
    from_mar_deep = os.path.join(path_to_fwop, "mar_deep", "predictors")
    to_mar_deep = os.path.join(path_to_alt, "mar_deep", "predictors")

    copy_tif(from_mar_deep, to_mar_deep, "vessel_density*")

    # mar_int ------------------------------------------------------------------
    arcpy.AddMessage("# MAR_INT")
    from_mar_int = os.path.join(path_to_fwop, "mar_int", "predictors")
    to_mar_int = os.path.join(path_to_alt, "mar_int", "predictors")

    copy_tif(from_mar_int, to_mar_int, "dev_100_per*")
    copy_tif(from_mar_int, to_mar_int, "shoreline_armoring*")
    copy_tif(from_mar_int, to_mar_int, "slope_per*")

    # mar_sub ------------------------------------------------------------------
    arcpy.AddMessage("# MAR_SUB")
    from_mar_sub = os.path.join(path_to_fwop, "mar_sub", "predictors")
    to_mar_sub = os.path.join(path_to_alt, "mar_sub", "predictors")

    copy_tif(from_mar_sub, to_mar_sub, "pct_fines*")
    copy_tif(from_mar_sub, to_mar_sub, "vessel_density*")


if __name__ == "__main__":
    # Get input parameters
    path_to_fwop = arcpy.GetParameterAsText(0)
    path_to_alt = arcpy.GetParameterAsText(1)

    main()
