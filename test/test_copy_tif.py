import pytest
import os
import nybem_tools.utils
import test_data


# Arrange
@pytest.fixture
def data_folder_1():
    return os.path.join(test_data.data_folder(), "folder_1")


@pytest.fixture
def data_folder_2():
    return os.path.join(test_data.data_folder(), "folder_2")


# Act
@pytest.fixture
def copy_tif_1(data_folder_1, data_folder_2):
    nybem_tools.utils.copy_tif(data_folder_1, data_folder_2, "file_*")


# Assert
def test_copy_tif_exists(data_folder_1, data_folder_2):
    assert os.path.exists(os.path.join(data_folder_2, "file_1.txt"))
    assert os.path.exists(os.path.join(data_folder_2, "file_2.txt"))
