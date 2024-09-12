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
    Traverse the data directory structure to find all label files and copy them to the model directory,
    updating the labels with the correct mapping for the final model.

    Args:
        data_dir (str): The root data directory.
        split_dirs (List[str], optional): A list of directory names to filter by. Defaults to ['train', 'test', 'valid'].
    """
    top_level_dirs = list_subdirectories(data_dir)
    print(f'Top Level Directories: \n {top_level_dirs}')
    
    for dir in top_level_dirs:
        # Load YAML data from old and new locations
        yaml_filepath = os.path.join(dir, 'data.yaml')
        directory = dir.split('/')[-1]
        
        if not os.path.exists(yaml_filepath):
            print(f"Skipping directory {dir}: 'data.yaml' not found.")
            continue
        
        # Create the label mapping
        lbl_mapping = create_label_mapping(get_yaml_data(yaml_filepath), get_yaml_data(model_yaml_path))
        
        # Loop through subdirectories ('train', 'test', 'valid')
        split_dirs = list_subdirectories(dir)
        for split_dir in split_dirs:
            split_name = split_dir.split('/')[-1]  # Get the directory name (train, test, or valid)

            if split_name not in ['train', 'test', 'valid']:
                continue

            # Loop through labels directory
            label_dirs = list_subdirectories(split_dir)[1]  # Gets only the labels directory (index 1)
            print(f'Label Directories: {label_dirs}')
            
            for file in os.listdir(label_dirs):
                filepath = os.path.join(label_dirs, file)
                
                # Update the label file using the label mapping
                txt_file = update_yolo_label_file(filepath, lbl_mapping)
                
                # Set the output directory based on the split_name
                output_dir = os.path.join(model_dir, split_name, 'labels')
                
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                output_filepath = os.path.join(output_dir, file)
                write_label_files(txt_file, output_filepath)

def main():
    get_label_file_paths(data_dir, ['train', 'test', 'valid'])

if __name__ == '__main__':
    main()
