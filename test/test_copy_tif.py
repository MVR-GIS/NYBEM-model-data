import pytest
import os
from nybem_tools.utils import copy_tif


@pytest.fixture
def run_copy_tif():
    path_to_folder_1 = r"\folder_1"
    path_to_folder_2 = r"\folder_2"
    copy_tif(path_to_folder_1, path_to_folder_2, "file_*")


def test_copy_tif():
    assert os.path.exists(r"\folder_2\file_1.txt")
    assert os.path.exists(r"\folder_2\file_2.txt")
