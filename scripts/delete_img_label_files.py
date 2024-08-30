import os
import logging
from dotenv import load_dotenv
from typing import List, Tuple

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Script variables
freiburg_dir = os.getenv('FREIBURG_DIR')
sub_dirs = ['test', 'train', 'valid']
classes_to_remove = ('BEANS', 'OIL', 'VINEGAR', 'SPICES')

def process_directories(img_lbl_dirs_path: str, classes: Tuple[str, ...]) -> None:
    """
    Removes files within each directory inside the given parent directory.

    Parameters:
    img_lbl_dirs_path (str): Path to the parent directory containing subdirectories.
    classes (Tuple[str, ...]): Tuple of class names to remove corresponding files.

    Returns:
    None
    """
    try:
        for data in os.listdir(img_lbl_dirs_path):
            data_dir_path = os.path.join(img_lbl_dirs_path, data)
            if os.path.isdir(data_dir_path):
                for filename in os.listdir(data_dir_path):
                    file_path = os.path.join(data_dir_path, filename)
                    if filename.startswith(classes):
                        os.remove(file_path)
                        logging.info(f"Removed: {file_path}")
                    else:
                        logging.info(f"Skipped filepath: {file_path} was not removed.")
            else:
                logging.warning(f"Skipped directory: {data_dir_path} is not a directory.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main(directory: str, sub_directory_list: List[str]) -> None:
    """
    Main function to process directories and remove specified classes of files.

    Parameters:
    directory (str): The root directory containing subdirectories.
    sub_directory_list (List[str]): List of subdirectory names to process.

    Returns:
    None
    """
    for dir_name in sub_directory_list:
        img_lbl_dirs_path = os.path.join(directory, dir_name)
        process_directories(img_lbl_dirs_path, classes_to_remove)

if __name__ == '__main__':
    main(freiburg_dir, sub_dirs)
