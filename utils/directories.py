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

def filter_directories_by_name(directories: List[str], names: List[str]) -> List[str]:
    """
    Filter a list of directories by matching directory names against a list of names.

    Args:
        directories (List[str]): A list of directory paths.
        names (List[str]): A list of names to filter directories by.

    Returns:
        List[str]: A list of filtered directory paths.
    """
    return [dir_path for dir_path in directories if os.path.basename(dir_path) in names]

def list_files_in_directory(directory: str, file_extension: str = None) -> List[str]:
    """
    List all files within a given directory, optionally filtering by file extension.

    Args:
        directory (str): The path to the directory to list files from.
        file_extension (str, optional): A file extension to filter files by. Defaults to None.

    Returns:
        List[str]: A list of file paths.
    """
    files = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    if file_extension:
        return [file for file in files if file.endswith(file_extension)]
    return files

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
        # Loop through subdirectories (e.g., 'train', 'test', 'valid')
        split_dirs = filter_directories_by_name(list_subdirectories(dir), split_dirs)

        for split_dir in split_dirs:
            # Loop through 'labels' directory
            label_dirs = filter_directories_by_name(list_subdirectories(split_dir), ['labels'])

            for label_dir in label_dirs:
                # List all label files
                label_files = list_files_in_directory(label_dir)
                label_file_paths.extend(label_files)

    return label_file_paths


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