# This script does a random split of the img_files and label files in train, test and valid folders of the yolo_model directory

import os
import sys
from typing import List, Tuple
import random

from dotenv import load_dotenv
import shutil
from pprint import pprint


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.images_util import get_image_label_pairs
from utils.directories_util import create_split_dirs

load_dotenv()
model_dir = os.getenv('MODEL_DIR')





def split_dataset(data: List[Tuple[str, str]], train_pct: float, valid_pct: float, seed: int) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Split the dataset into train, validation, and test sets based on the given percentages.
    Returns: 
        Tuple[List[Tuple[str, str]], List[Tuple[str, str]], List[Tuple[str, str]]]: Tuple of Lists to each path for each split set
    """
    random.seed(seed)
    random.shuffle(data)
    
    train_end = int(train_pct * len(data))
    valid_end = int(valid_pct * len(data)) + train_end
    
    train_data = data[:train_end]
    valid_data = data[train_end:valid_end]
    test_data = data[valid_end:]
    
    return train_data, valid_data, test_data

def copy_files(data: List[Tuple[str, str]], split_dir: str):
    """
    Copy image and label files to the appropriate split directory.
    """
    add_count = 0
    skipped_count = 0
    for image_path, label_path in data:
        image_dest = os.path.join(split_dir, 'images', os.path.basename(image_path))
        label_dest = os.path.join(split_dir, 'labels', os.path.basename(label_path))
        
        if image_path != image_dest:
            try:
                # Copy file to destination
                shutil.copy(image_path, image_dest)
                shutil.copy(label_path, label_dest)
                print(f"Copied: {label_path} to {label_dest}")
            except FileNotFoundError as e:
                print(f"Error copying file {label_path}: {e}")
            except Exception as e:
                print(f"Unexpected error copying file {label_path}: {e}")
            add_count += 1
        else:
            skipped_count += 1
    print(f'Added {add_count} files. in {split_dir} Directory')
    print(f'Skipped {skipped_count} files. in {split_dir} Directory')

def main():
    model_dir = 'yolo_model'
    images_dir = os.path.join(model_dir, 'train', 'images')
    labels_dir = os.path.join(model_dir, 'train', 'labels')
    
    create_split_dirs(model_dir)
    
    image_label_pairs = get_image_label_pairs(images_dir)
    
    train_data, valid_data, test_data = split_dataset(image_label_pairs, train_pct=0.80, valid_pct=0.15, seed=123)
    
    copy_files(train_data, os.path.join(model_dir, 'train'))
    copy_files(valid_data, os.path.join(model_dir, 'valid'))
    copy_files(test_data, os.path.join(model_dir, 'test'))

if __name__ == '__main__':
    main()