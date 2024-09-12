# Utilities to manipulate yaml files

import os
import yaml
from typing import List, Dict
from pprint import pprint


def get_yaml_data(yaml_file: str) -> Dict[int, str]:
    """
    Open yaml file from yaml path.

    Args:
        data_dir (str): YAML file to be opened.

    Returns:
        Dict[int, str]: A dictionary with the name mappings from a YAML file
    """
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    if isinstance(data['names'], list):
        # Case for old yaml_files without dict list
        class_name_dict = {k:v for k, v in enumerate(data['names'])}
    elif isinstance(data['names'], dict):
        class_name_dict = dict(data['names'])
    else:
        print('Not Correct Data type')
    return class_name_dict



def create_label_mapping(old_classes: Dict[int, str], new_classes: Dict[int, str]):
    """
    Create a dictionary mapping old class labels to new class labels.
    
    Args:
        old_classes Dict[int, str]: List of old class names.
        new_classes Dict[int, str]: List of new class names.
    
    Returns:
        Dict[int, str]: A mapping of old class indices to new class indices.
    """
    # pprint(f'Old dictionary: \n {old_classes}')
    # pprint(f'New dictionary: \n {new_classes}')

    label_mapping = {}
    new_classes_reversed = {v: k for k, v in new_classes.items()}
    
    for old_idx, old_class in old_classes.items():
        if old_class in new_classes_reversed:
            new_idx = new_classes_reversed[old_class]
            label_mapping[old_idx] = new_idx
        else:
            print(f"Warning: {old_class} not found in new_classes")
    return label_mapping



def main():
      pass


if __name__ == '__main__':
      main()