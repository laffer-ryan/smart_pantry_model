import numpy as np
import torch
import cv2
import os
from ultralytics import YOLO
from dotenv import load_dotenv

import logging

logging.basicConfig(
    filename='object_movement_and_inventory.log',  # Log file name
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

# Inventory list to keep track of objects
inventory = set()


# Display predictions on a frame
def display_predictions(frame, predictions):
    """
    Draw bounding boxes and labels on the video frame.
    
    Args:
        frame (np.ndarray): The frame on which to draw the predictions.
        predictions: YOLO model predictions containing bounding boxes and labels.
    
    Returns:
        np.ndarray: The annotated frame with bounding boxes and labels.
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
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Add label and confidence
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

    return frame

# Load model from NCNN folder
def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path {model_path} does not exist.")
    return YOLO(model_path)

def get_quadrant(center_x, center_y, frame_width, frame_height):
    """
    Determine which quadrant the point (center_x, center_y) is in.
    """
    # Two sides of frame
    if center_x < frame_width / 2:
        return 'A' # Left side
    else:
        return 'B' # Right side

    # # Four Quadrants of frame
    # if center_x < frame_width / 2:  
    #     if center_y < frame_height / 2:
    #         return 'A'  # Top left 
    #     else:
    #         return 'B'  # Bottom left 
    # else: 
    #     if center_y < frame_height / 2:
    #         return 'C'  # Top right 
    #     else:
    #         return 'D'  # Bottom right 

# Following function needs to interact with sqldb
def update_inventory(object_id, new_quadrant):
    """
    Update inventory based on object movement between quadrants.
    """
    if new_quadrant == 'B' and object_id in inventory:
        inventory.remove(object_id)
        logging.info(f"Removed {object_id} from inventory. Moved to quadrant {new_quadrant}.")
    elif new_quadrant == 'A' and object_id not in inventory:
        inventory.add(object_id)
        logging.info(f"Added {object_id} to inventory. Moved to quadrant {new_quadrant}.")

def log_movement(object_id, prev_quadrant, new_quadrant):
    """
    Log the movement of an object between quadrants.
    """
    logging.info(f"Object '{object_id}' moved from quadrant {prev_quadrant} to {new_quadrant}.")

def main():
    model_path = os.getenv('BEST_MODEL_PATH')
    video_path = os.getenv('TEST_VIDEO_PATH')  # Update this to your video file
    output_video_path = os.getenv('OUTPUT_VIDEO_PATH')  # Path to save the output video

    # Load the YOLO model and video
    model = load_model(model_path)
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        raise FileNotFoundError(f"Video file {video_path} not found or cannot be opened.")

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Init VideoWriter to save output video
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Parameters for Lucas-Kanade optical flow
    lk_params = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Initialize variables for optical flow
    prev_gray = None
    prev_points = None
    prev_predictions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Make predictions on the current frame
        results = model.predict(source=frame)

        # Get predictions if they exist
        predictions = []
        current_points = []
        current_quadrants = {}
        for result in results:
            if (len(result.boxes.xyxy) > 0) and (result.boxes.conf[0].item() > .60):  # Check if there are any detections and confidence level is > 60%
                box = result.boxes.xyxy[0].tolist()
                class_id = result.names[result.boxes.cls[0].item()]
                confidence = result.boxes.conf[0].item()
                predictions.append({
                    'box': box,
                    'confidence': confidence,
                    'class': class_id
                })

                # Find center of the box and add to list
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                current_points.append((center_x, center_y))
                current_quadrants[class_id] = get_quadrant(center_x, center_y, frame_width, frame_height)

        # Optical flow 
        if prev_gray is not None and prev_points is not None and len(prev_points) > 0:
            current_points_np = np.array(current_points, dtype=np.float32).reshape(-1, 2)
            prev_points_np = np.array(prev_points, dtype=np.float32).reshape(-1, 2)

            # Calculate optical flow 
            next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points_np, current_points_np, **lk_params)

            logging.info(f"Next Points: {next_points}")

            if next_points is not None:
                # Track object movement and update inventory
                for i in range(min(len(prev_points_np), len(predictions))):
                    prev_pt = prev_points_np[i]
                    next_pt = next_points[i]

                    logging.info(f'Previous Point: {prev_pt} - Next Point: {next_pt}')

                    prev_class_id = prev_predictions[i]['class']
                    logging.info(f"Prev Class ID: {prev_class_id}")
                    prev_quadrant = current_quadrants[prev_class_id]
                    new_x, new_y = next_pt.ravel()
                    new_quadrant = get_quadrant(new_x, new_y, frame_width, frame_height)

                    if prev_quadrant != new_quadrant:
                        log_movement(prev_class_id, prev_quadrant, new_quadrant)
                        update_inventory(prev_class_id, new_quadrant)
            else:
                logging.error("Optical flow calculation failed. 'next_points' is None.")


        # Annotate frame with predictions
        annotated_frame = display_predictions(frame, predictions)

        # Write the annotated frame to the output video
        out.write(annotated_frame)

        # Optionally, display the frame
        cv2.imshow("Smart Pantry Predictions", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Update previous frame and points
        prev_gray = gray
        prev_points = current_points
        prev_predictions = predictions

    # Release video capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
