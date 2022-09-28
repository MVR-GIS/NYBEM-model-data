import pytest
import os
import arcpy
import test_data
import nybem_tools.utils


# Arrange
test_data.license_arcpy()


@pytest.fixture(scope="module")
def output_folder():
    return os.path.join(test_data.data_folder(), "outputs")


@pytest.fixture(scope="module")
def wse_100():
    return os.path.join(test_data.data_folder(), "folder_1", "wse_100.tif")


@pytest.fixture(scope="module")
def wse_0():
    return os.path.join(test_data.data_folder(), "folder_1", "wse_0.tif")


@pytest.fixture(scope="module")
def wse_mhhw():
    return os.path.join(test_data.data_folder(), "folder_1", "mhhw.tif")


@pytest.fixture(scope="module")
def wse_mllw():
    return os.path.join(test_data.data_folder(), "folder_1", "mllw.tif")


# Act
@pytest.fixture(scope="module")
def output_raster_1(output_folder, wse_100, wse_0, wse_mhhw, wse_mllw):
    output_name = "expo_dur"

    nybem_tools.utils.expo_dur(output_folder, output_name,
                               wse_100, wse_0, wse_mhhw, wse_mllw)
    return os.path.join(output_folder, "expo_dur.tif")


# Assert
def test_depth_1_exists(output_raster_1):
    assert os.path.exists(output_raster_1)


def test_depth_1_dims(output_raster_1):
    assert arcpy.arcpy.GetRasterProperties_management(
                       output_raster_1, "COLUMNCOUNT").getOutput(0) == "376"
    assert arcpy.arcpy.GetRasterProperties_management(
                       output_raster_1, "ROWCOUNT").getOutput(0) == "428"
    assert arcpy.arcpy.GetRasterProperties_management(
                       output_raster_1, "CELLSIZEX").getOutput(0) == "10"
