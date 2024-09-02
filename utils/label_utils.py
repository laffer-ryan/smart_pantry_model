# Utilities to manipulate yolo label files

import os
import yaml
from typing import List, Dict


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

def update_yolo_label_file(label_file_path, label_mapping):
    """
    Update a YOLO label file with new class indices based on the given mapping.
    
    Args:
        label_file_path (str): Path to the YOLO label file.
        label_mapping (dict): Mapping of old class indices to new class indices.
    """
    updated_lines = []
    with open(label_file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        parts = line.strip().split()
        old_class_idx = int(parts[0])
        
        # Map the old class index to the new class index
        if old_class_idx in label_mapping:
            new_class_idx = label_mapping[old_class_idx]
            # Replace the old index with the new one
            parts[0] = str(new_class_idx)
            updated_line = ' '.join(parts)
            updated_lines.append(updated_line)
        else:
            print(f"Warning: Old class index {old_class_idx} not found in label mapping.")
    
    return updated_lines


def write_label_files(txt_file: str, output_file_path: str) -> None:
    """
    Write label files to output directory.
    
    Args:
        txt_file (str): Line from updated text file.
        output_file_path (str): path to the output file 
    """
    # Write the updated lines back to the file
    with open(output_file_path, 'w') as file:
        file.write("\n".join(txt_file) + "\n")
    
    return None

def update_bbox_dims():
    """
    Should be used to update bbox dimensions based on scale provided by images_util.scale_images
    """
    pass