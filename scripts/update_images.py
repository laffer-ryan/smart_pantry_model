
import os
import sys
from dotenv import load_dotenv
import shutil
from pprint import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.directories_util import *

load_dotenv()
data_dir = os.getenv('DATA_DIR')
model_dir = os.getenv('MODEL_DIR')


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
        # Loop through subdirectories ('train', 'test', 'valid')
        split_dirs = list_subdirectories(dir)
        for split_dir in split_dirs:
            # Loop through 'images' directory
            image_files = list_subdirectories(split_dir)[0]
            for image_file in os.listdir(image_files):
                image_filepath = os.path.join(image_files, image_file)

                print(f'image_filepath: \n {image_filepath}')

                output_dir = os.path.join(model_dir, 'train', 'images')

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_filepath = os.path.join(output_dir, image_file)
                shutil.copy(image_filepath, output_filepath)
            


get_label_file_paths(data_dir, ['train', 'test', 'valid'])



