import os
import numpy as np

def check_labels(directory, num_classes):
    """
    Function to check for inappropriate data in YOLO label files.
    
    Parameters:
        directory (str): Directory containing the label files (train, valid, or test).
        num_classes (int): Number of classes in the dataset.
    """
    errors_found = False
    label_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    for label_file in label_files:
        file_path = os.path.join(directory, label_file)
        
        try:
            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                print(f"Error: Empty label file found - {file_path}")
                errors_found = True
                continue
            
            # Load the label file
            labels = np.loadtxt(file_path, ndmin=2)
            
            for label in labels:
                # Check if the label has 5 elements (class index, x_center, y_center, width, height)
                if len(label) != 5:
                    print(f"Error: Invalid label format in file - {file_path}")
                    errors_found = True
                    continue
                
                class_index, x_center, y_center, width, height = label
                
                # Check if class index is within the valid range
                if not (0 <= class_index < num_classes):
                    print(f"Error: Class index out of bounds in file - {file_path}. Found {class_index}, but should be in range [0, {num_classes - 1}]")
                    errors_found = True
                
                # Check if bounding box coordinates are within the valid range (0 to 1)
                if not (0 <= x_center <= 1) or not (0 <= y_center <= 1) or not (0 <= width <= 1) or not (0 <= height <= 1):
                    print(f"Error: Bounding box coordinates out of range in file - {file_path}. Found ({x_center}, {y_center}, {width}, {height})")
                    errors_found = True

                # Check for NaN or Inf values
                if np.isnan(label).any() or np.isinf(label).any():
                    print(f"Error: NaN or Inf value found in file - {file_path}")
                    errors_found = True
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            errors_found = True
    
    if not errors_found:
        print(f"No errors found in {directory}.")

if __name__ == "__main__":
    # Replace these paths with your actual dataset directories
    directories = [
        "/Users/laffer/Desktop/smart_pantry_model/yolo_model/train/labels",
        "/Users/laffer/Desktop/smart_pantry_model/yolo_model/test/labels", 
        "/Users/laffer/Desktop/smart_pantry_model/yolo_model/valid/labels"]
    num_classes = 109  #
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"Checking labels in directory: {directory}")
            check_labels(directory, num_classes)
        else:
            print(f"Directory not found: {directory}")
