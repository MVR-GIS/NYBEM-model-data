import pytest
import os
import test_data
import nybem_tools.utils


# Arrange
test_data.license_arcpy()

@pytest.fixture
def output_folder():
    return os.path.join(test_data.data_folder(), "outputs")

@pytest.fixture
def output_name():
    return "vel_10"

@pytest.fixture
def adh_points():
    return os.path.join(test_data.data_folder(), "adh", "velocity.shp")

@pytest.fixture
def variable():
    return "vel_10"

@pytest.fixture
def sql_select():
    return ""

@pytest.fixture
def barriers():
    return os.path.join(test_data.data_folder(), "example_data.gdb", "barriers")

@pytest.fixture
def mask():
    return os.path.join(test_data.data_folder(), "mask_10m.tif")


def test_adh2raster_1(output_folder, output_name, adh_points,
                      variable, sql_select, barriers, mask):
    # Act
    nybem_tools.utils.adh2raster(output_folder, output_name, adh_points,
                                 variable, sql_select, barriers, mask)

    # Assert
    assert os.path.exists(os.path.join(output_folder, "vel_10.tif"))
