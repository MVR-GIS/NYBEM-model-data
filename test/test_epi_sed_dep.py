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
def wse_mhhw():
    return os.path.join(test_data.data_folder(), "folder_1", "mhhw.tif")


@pytest.fixture(scope="module")
def wse_median():
    return os.path.join(test_data.data_folder(), "folder_1", "wse_median.tif")


@pytest.fixture(scope="module")
def wse_max():
    return os.path.join(test_data.data_folder(), "folder_1", "wse_100.tif")


# Act
@pytest.fixture(scope="module")
def output_raster_1(output_folder, wse_mhhw, wse_median, wse_max):
    output_name = "esd"

    nybem_tools.utils.epi_sed_dep(output_folder, output_name,
                                  wse_mhhw, wse_median, wse_max)
    return os.path.join(output_folder, "esd.tif")


# Assert
def test_esd_1_exists(output_raster_1):
    assert os.path.exists(output_raster_1)


def test_esd_1_dims(output_raster_1):
    assert arcpy.arcpy.GetRasterProperties_management(
                       output_raster_1, "COLUMNCOUNT").getOutput(0) == "376"
    assert arcpy.arcpy.GetRasterProperties_management(
                       output_raster_1, "ROWCOUNT").getOutput(0) == "428"
    assert arcpy.arcpy.GetRasterProperties_management(
                       output_raster_1, "CELLSIZEX").getOutput(0) == "10"
