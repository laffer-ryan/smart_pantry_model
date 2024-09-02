# Library for functionality and manipulation of images for output YOLO files

import os
from typing import List, Tuple
from PIL import Image
from pprint import pprint



def get_img_size(img_path):
    img = Image.open(img_path)
    # Get original image size
    img_size = img.size
    return img_size



def convert_imgpath_to_labelpath(img_filepath: str) -> str:
    """
    Converts an img file path to a label file path

    Returns:
        Label filepath
    """
    label_filepath = img_filepath.replace('.jpg', '.txt').replace('images', 'labels')

    return label_filepath

def get_image_label_pairs(images_dir: str) -> List[Tuple[str, str]]:
    """
    Get a list of tuples containing image file paths and corresponding label file paths.
    """
    image_files = sorted(os.listdir(images_dir))
    # label_files = sorted(os.listdir(labels_dir))
    

    return [(os.path.join(images_dir, img), convert_imgpath_to_labelpath(os.path.join(images_dir, img))) for img in image_files]


tuple_list = get_image_label_pairs('/Users/laffer/Desktop/smart_pantry_model/yolo_model/train/images')

assert tuple_list[0] != tuple_list[1]

pprint(tuple_list)