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


@pytest.fixture(scope="module")
def output_raster_2():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "mhhw"
    adh_points = os.path.join(test_data.data_folder(), "adh", "wse.shp")
    variable = "MHHW"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "mhhw.tif")


@pytest.fixture(scope="module")
def output_raster_3():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "wse_median"
    adh_points = os.path.join(test_data.data_folder(), "adh", "wse.shp")
    variable = "wse_50"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "wse_median.tif")


@pytest.fixture(scope="module")
def output_raster_4():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "wse_100"
    adh_points = os.path.join(test_data.data_folder(), "adh", "wse.shp")
    variable = "wse_100"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "wse_100.tif")


@pytest.fixture(scope="module")
def output_raster_5():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "wse_mtl"
    adh_points = os.path.join(test_data.data_folder(), "adh", "wse.shp")
    variable = "Mean_WSE"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "wse_mtl.tif")


@pytest.fixture(scope="module")
def output_raster_6():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "bed_elevation"
    adh_points = os.path.join(test_data.data_folder(), "adh", "elevation.shp")
    variable = "Elevation"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "bed_elevation.tif")


@pytest.fixture(scope="module")
def output_raster_7():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "mllw"
    adh_points = os.path.join(test_data.data_folder(), "adh", "wse.shp")
    variable = "MLLW"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "mllw.tif")


@pytest.fixture(scope="module")
def output_raster_8():
    output_folder = os.path.join(test_data.data_folder(), "outputs")
    output_name = "wse_0"
    adh_points = os.path.join(test_data.data_folder(), "adh", "wse.shp")
    variable = "wse_0"
    sql_select = ""
    barriers = os.path.join(test_data.data_folder(), "example_data.gdb",
                            "barriers")
    mask = os.path.join(test_data.data_folder(), "mask_10m.tif")

    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)
    return os.path.join(output_folder, "wse_0.tif")


# Assert
def test_adh_raster_1_exists(output_raster_1):
    assert os.path.exists(output_raster_1)


def test_adh_raster_2_exists(output_raster_2):
    assert os.path.exists(output_raster_2)


def test_adh_raster_3_exists(output_raster_3):
    assert os.path.exists(output_raster_3)


def test_adh_raster_4_exists(output_raster_4):
    assert os.path.exists(output_raster_4)


def test_adh_raster_5_exists(output_raster_5):
    assert os.path.exists(output_raster_5)


def test_adh_raster_6_exists(output_raster_6):
    assert os.path.exists(output_raster_6)


def test_adh_raster_7_exists(output_raster_7):
    assert os.path.exists(output_raster_7)


def test_adh_raster_8_exists(output_raster_8):
    assert os.path.exists(output_raster_8)


def test_adh_raster_1_dims(output_raster_1):
    assert arcpy.GetRasterProperties_management(
                       output_raster_1, "COLUMNCOUNT").getOutput(0) == "376"
    assert arcpy.GetRasterProperties_management(
                       output_raster_1, "ROWCOUNT").getOutput(0) == "428"
    assert arcpy.GetRasterProperties_management(
                       output_raster_1, "CELLSIZEX").getOutput(0) == "10"
