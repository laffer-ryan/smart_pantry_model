# Utilities to manipulate yolo label files

import os
import yaml
from typing import List, Dict
from pprint import pprint


def get_labelfile_data(label_filepath: str):
    """
    Open label file from path.

    Args:
        label_filepath (str): Path to YOLO label file.

    Returns:
        
    """
    with open(label_filepath, 'r') as file:
        lines = file.readlines()
    return lines