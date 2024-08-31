
import numpy as np
import pandas as pd
import yaml
import os
import sys
from dotenv import load_dotenv
from pprint import pprint


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.directories import *
from utils.yaml_utils import *
from utils.label_utils import *

load_dotenv()

data_dir = os.getenv('DATA_DIR')
model_dir = os.getenv('MODEL_DIR')
model_yaml_path = os.path.join(model_dir, 'data.yaml')

def get_label_file_paths(data_dir: str, split_dirs: List[str] = ['train', 'test', 'valid']) -> List[str]:
    """
    Traverse the data directory structure to find all label files.

    Args:
        data_dir (str): The root data directory.
        split_dirs (List[str], optional): A list of directory names to filter by. Defaults to ['train', 'test', 'valid'].

    Returns:
        List[str]: A list of paths to label files.
    """
    label_file_paths = []

    # Loop through top-level directories
    top_level_dirs = list_subdirectories(data_dir)
    print(f'Top Level Directories: \n {top_level_dirs}')
    for dir in top_level_dirs:
        # Load YAML data from old and new locations
        yaml_filepath = os.path.join(dir, 'data.yaml')
        lbl_mapping = create_label_mapping(get_yaml_data(yaml_filepath), get_yaml_data(model_yaml_path))

        # Loop through subdirectories ('train', 'test', 'valid')
        list_subdirectories
        print(f'List Sub Dirs: \n {list_subdirectories(dir)}')

        split_dirs = list_subdirectories(dir)
        for split_dir in split_dirs:
            # Loop through 'labels' directory
            label_dirs = list_subdirectories(split_dir)[1]  # Gets only the index 1 which contains the labels and not images directory
            for file in os.listdir(label_dirs):
                filepath = os.path.join(label_dirs, file)
                pprint(f'Updated Yolo Files: \n {update_yolo_label_file(filepath, lbl_mapping)}')
                pprint(f'Label Map: \n {lbl_mapping}')


    return None


label_file_paths = get_label_file_paths(data_dir, ['train', 'test', 'valid'])


# lines = get_labelfile_data('/Users/laffer/Desktop/smart_pantry_model/IMG_0244_JPEG.rf.3a00b2a4f23be36f96b3e1bad95a599c.txt')
# pprint(lines)



