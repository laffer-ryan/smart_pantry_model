
import json
import yaml
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

data_dir = os.getenv('DATA_DIR')
final_model_dir = os.getenv('MODEL_DIR')



def get_yaml_file_paths(data_dir: str) -> List[str]:
    """
    Retrieve the paths to all 'data.yaml' files within subdirectories of a given directory.

    Args:
        data_dir (str): The root directory containing subdirectories to search for 'data.yaml' files.

    Returns:
        List[str]: A list of file paths to 'data.yaml' files found within the subdirectories.
    """
    # Verify the directory exists
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"The directory '{data_dir}' does not exist.")
    
    # Ensure the input path is a directory
    if not os.path.isdir(data_dir):
        raise ValueError(f"The path '{data_dir}' is not a directory.")

    yaml_files = []
    
    # Iterate through each subdirectory in the given directory
    for dir_name in os.listdir(data_dir):
        directory = os.path.join(data_dir, dir_name)
        
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename == 'data.yaml':
                    yaml_path = os.path.join(directory, filename)
                    yaml_files.append(yaml_path)

    return yaml_files

def get_yaml_data(yaml_files: List[str]) -> List:
    """
    Load data from each yaml file

    Args:
        yaml_files: list of yaml file paths
    Returns:
        List of unique classes from all data.yaml file in data directory
    """
    loaded_yaml_data = []
    # Loop through each file path and load the YAML content
    for file_path in yaml_files:
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
            # print(yaml_data['names'])
            loaded_yaml_data.extend(yaml_data['names'])
    classes_list = list(set(loaded_yaml_data))
    classes_list.sort()
    return classes_list

def create_class_dict(classes_list: List[str]) -> Dict[int, str]:
    """
    Converts a list of classes into a dictionary of indexed pairs.

    Args: 
        classes_list (List[str]): List of unique classes to create the dictionary.

    Returns:
        Dict[int, str]: A dictionary where keys are indices and values are class names.
    """
    classes_dict = dict()
    for i, cls in enumerate(classes_list):
        classes_dict[i] = cls
    return classes_dict

def create_yaml_file(classes_dict: Dict[int, str], output_dir: str) -> None:
    """
    Creates a YAML file with the specified structure, where the 'nc' and 'names' 
    fields are derived from the provided classes_dict.

    Args:
        classes_dict (Dict[int, str]): A dictionary where keys are indices and values are class names.
        output_path (str): The directory path where the YAML file will be saved.

    Returns:
        None
    """
    output_file = os.path.join(output_dir, 'data.yaml')

    nc = len(classes_dict)
    
    names = {k: v for k, v in classes_dict.items()}
    
    data = {
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': nc,
        'names': names
    }
    
    with open(output_file, 'w') as yaml_file:
        yaml.dump(data, yaml_file)

    print(f"YAML file created at: {output_file}")



def main(data_dir: str) -> None:
    """
    Main function for program runs all functions in sequence
    """
    yaml_files = get_yaml_file_paths(data_dir=data_dir)
    classes_list = get_yaml_data(yaml_files)
    classes_dict = create_class_dict(classes_list)
    create_yaml_file(classes_dict, final_model_dir)
    print(classes_dict)

main(data_dir=data_dir)




