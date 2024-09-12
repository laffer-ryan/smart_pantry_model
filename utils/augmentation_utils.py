import os
import shutil
import random

def oversample_class(class_dir, target_size):
    """
    Oversample a class by duplicating its images until it reaches the target size.
    
    Args:
        class_dir (str): Directory containing images of the class to oversample.
        target_size (int): Desired number of images after oversampling.
    """
    images = os.listdir(class_dir)
    current_size = len(images)
    
    if current_size >= target_size:
        print(f"Class already has {current_size} images. No oversampling needed.")
        return
    
    while len(images) < target_size:
        img_to_duplicate = random.choice(images)
        new_img_name = f"{os.path.splitext(img_to_duplicate)[0]}_dup{len(images)}.jpg"
        shutil.copy(os.path.join(class_dir, img_to_duplicate), os.path.join(class_dir, new_img_name))
        images.append(new_img_name)
