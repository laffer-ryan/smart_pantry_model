# This script creates the directory for label files for the final model
# This scripts takes the label mapping and finalized yaml file and convert the label files to the correct mapping for the final model
# This script then copies the file to 

import yaml
import os
import sys
from dotenv import load_dotenv
import shutil
from pprint import pprint


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.directories_util import *
from utils.yaml_utils import *
from utils.label_utils import *

load_dotenv()

data_dir = os.getenv('DATA_DIR')
model_dir = os.getenv('MODEL_DIR')
model_yaml_path = os.path.join(model_dir, 'data.yaml')

def get_label_file_paths(data_dir: str, split_dirs: List[str] = ['train', 'test', 'valid']):
    """
    Traverse the data directory structure to find all label files and copies label files to model directory

    Args:
        data_dir (str): The root data directory.
        split_dirs (List[str], optional): A list of directory names to filter by. Defaults to ['train', 'test', 'valid'].

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
                txt_file = update_yolo_label_file(filepath, lbl_mapping)
                output_dir = os.path.join(model_dir, 'train', 'labels')

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_filepath = os.path.join(output_dir, file)
                write_label_files(txt_file, output_filepath)




get_label_file_paths(data_dir, ['train', 'test', 'valid'])



