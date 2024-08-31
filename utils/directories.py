# Utilities to get to specific directory levels

import os
from typing import List

def list_subdirectories(directory: str) -> List[str]:
    """
    List all subdirectories within a given directory.

    Args:
        directory (str): The path to the directory to list subdirectories from.

    Returns:
        List[str]: A list of paths to subdirectories.
    """
    return [os.path.join(directory, sub_dir) for sub_dir in os.listdir(directory) if os.path.isdir(os.path.join(directory, sub_dir))]


def list_files_in_directory(directory: str, file_extension: str = None) -> List[str]:
    """
    List all files within a given directory, optionally filtering by file extension.

    Args:
        directory (str): The path to the directory to list files from.
        file_extension (str, optional): A file extension to filter files by. Defaults to None.

    Returns:
        List[str]: A list of file paths.
    """
    files = [os.path.join(directory, file) for file in os.listdir(directory) if (os.path.isfile(os.path.join(directory, file))) & (os.path)]
    if file_extension:
        return [file for file in files if file.endswith(file_extension)]
    return files



def get_yaml_file_paths(data_dir: str) -> List[str]:
    """
    Traverse the data directory structure to find all label files.

    Args:
        data_dir (str): The root data directory.

    Returns:
        List[str]: A list of paths to label files.
    """
    yaml_file_paths = []

    # Loop through top-level directories
    top_level_dirs = list_subdirectories(data_dir)
    # print(f'Top Level Dirs: {top_level_dirs}')
    
    [yaml_file_paths.append(os.path.join(dir, 'data.yaml')) for dir in top_level_dirs]

    return yaml_file_paths





### Directory Function
def main():
    pass
if __name__ == '__main__':
    main()