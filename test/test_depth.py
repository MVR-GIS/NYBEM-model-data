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
def wse_mtl():
    return os.path.join(test_data.data_folder(), "folder_1", "wse_mtl.tif")


@pytest.fixture(scope="module")
def bed_elevation():
    return os.path.join(test_data.data_folder(), "folder_1", "bed_elevation.tif")


# Act
@pytest.fixture(scope="module")
def output_raster_1(output_folder, wse_mtl, bed_elevation):
    output_name = "depth"

    nybem_tools.utils.depth(output_folder, output_name,
                            wse_mtl, bed_elevation)
    return os.path.join(output_folder, "depth.tif")


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
