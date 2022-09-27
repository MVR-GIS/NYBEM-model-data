import pytest
import os
from nybem_tools.utils import copy_tif
from test_data import data_folder

# Arrange
@pytest.fixture
def data_folder_1():
    return os.path.join(data_folder(), "folder_1")

@pytest.fixture
def data_folder_2():
    return os.path.join(data_folder(), "folder_2")


def test_copy_tif_1(data_folder_1, data_folder_2):
    # Act
    copy_tif(data_folder_1, data_folder_2, "file_*")

    # Assert
    assert os.path.exists(os.path.join(data_folder_2, "file_1.txt"))
    assert os.path.exists(os.path.join(data_folder_2, "file_2.txt"))

