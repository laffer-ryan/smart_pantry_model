import numpy as np
import torch
import cv2
import os
import yaml
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()


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

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Make predictions on the current frame
        results = model.predict(source=frame)

        # Get predictions if they exist
        predictions=[]
        for result in results:
            if (len(result.boxes.xyxy) > 0) and (result.boxes.conf[0].item() > .60):  # Check if there are any detections
                predictions.append({
                    'box': result.boxes.xyxy[0].tolist(),  # bounding box (x1, y1, x2, y2)
                    'confidence': result.boxes.conf[0].item(),  # confidence score
                    'class': result.names[result.boxes.cls[0].item()]  # predicted class
                })

        # Annotate frame with predictions
        if predictions:
            annotated_frame = display_predictions(frame, predictions)
        else:
            annotated_frame = frame #Pass the frame if there are no predictions
        # Write the annotated frame to the output video
        out.write(annotated_frame)

        # Optionally, display the frame
        cv2.imshow("Smart Pantry Predictions", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
