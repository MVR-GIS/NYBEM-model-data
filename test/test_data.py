"""This module contains functions used for testing
"""


"""Returns the full path to the test data folder
"""
def data_folder():
    import os

    test_abs_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_abs_path, "data")
