import numpy as np
import ncnn
import torch

import cv2
import numpy as np
from ultralytics import YOLO
import os
import yaml
from dotenv import load_dotenv

load_dotenv()


# Display predictions on image
def display_predictions(image, predictions, save_path=None):
    """
    Draw bounding boxes and labels on the image.
    
    Args:
        image (np.ndarray): The image on which to draw the predictions.
        predictions: YOLO model predictions containing bounding boxes and labels.
        save_path (str): If provided, the annotated image will be saved to this path.
    
    Returns:
        np.ndarray: The annotated image with bounding boxes and labels.
    """
    for pred in predictions:
        # Unpack prediction data (bounding box, confidence score, and class name)
        box = pred['box']
        class_id = pred['class']
        conf = pred['confidence']
        label = f"{class_id}: {conf:.2f}"

        # Get coordinates
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Add label and confidence
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

    if save_path:
        cv2.imwrite(save_path, image)

    return image

def load_model(model_path):
    """
    Load YOLO model from a specified NCNN directory.

    Args:
        model_path (str): Path to the YOLO NCNN model folder containing NCNN files.
    
    Returns:
        model: Loaded YOLO model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path {model_path} does not exist.")
    
    # Load YOLO model
    return YOLO(model_path)

def main():
    model_path = os.getenv('NCNN_MODEL_PATH')
    image_path = '/Users/laffer/Desktop/smart_pantry_model/data/my_pantry/train/images/20240829_181545_jpg.rf.a0cc0daa7d74e15fa4c810a83774949f.jpg'

    # Load the YOLO model and image
    model = load_model(model_path)
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image file {image_path} not found.")

    # Make predictions on the image
    results = model.predict(source=image_path)

    # Extract predictions (you may need to adjust based on the result format)
    predictions = [
        {
            'box': result.boxes.xyxy[0].tolist(),  # bounding box (x1, y1, x2, y2)
            'confidence': result.boxes.conf[0].item(),  # confidence score
            'class': result.names[result.boxes.cls[0].item()]  # predicted class
        }
        for result in results
    ]
    print(f'Predictions: {predictions}')
    # Display and save the predictions on the image
    annotated_image = display_predictions(image, predictions)

    # Show the image with predictions
    cv2.imshow("YOLO Predictions", annotated_image)
    cv2.waitKey(0)  # Wait for key press to close the image window
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
