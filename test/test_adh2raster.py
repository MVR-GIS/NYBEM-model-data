import pytest
import os
import arcpy
import test_data
import nybem_tools.utils


# Arrange
test_data.license_arcpy()


# Act
@pytest.fixture(scope="module")
def output_raster_1():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "vel_10"
    adh_points = os.path.join(test_data.data_folder(), "adh", "velocity.shp")
    variable = "vel_10"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "vel_10.tif")


# Assert
def test_adh_raster_exists(output_raster_1):
    assert os.path.exists(output_raster_1)


def test_adh_raster_dims(output_raster_1):
    assert arcpy.GetRasterProperties_management(
                       output_raster_1, "COLUMNCOUNT").getOutput(0) == "376"
    assert arcpy.GetRasterProperties_management(
                       output_raster_1, "ROWCOUNT").getOutput(0) == "428"
    assert arcpy.GetRasterProperties_management(
                       output_raster_1, "CELLSIZEX").getOutput(0) == "10"