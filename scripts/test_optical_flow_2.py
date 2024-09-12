import numpy as np
from datetime import datetime, timedelta
import torch
import cv2
import os
import sqlite3
from ultralytics import YOLO
from dotenv import load_dotenv

import logging

logging.basicConfig(
    filename='object_movement_and_inventory.log',  # Log file name
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

# Initialize SQLite database connection
conn = sqlite3.connect('object_movement.db')
cursor = conn.cursor()

def create_db():
    """Create a table for transactions"""
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id TEXT,
                    movement INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()

def display_predictions(frame, predictions):
    """
    Display predictions on a frame
    """
    for pred in predictions:
        box = pred['box']
        class_id = pred['class']
        conf = pred['confidence']
        label = f"{class_id}: {conf:.2f}"
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
    return frame

def load_model(model_path):
    """
    Load model from NCNN folder
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path {model_path} does not exist.")
    return YOLO(model_path)

def get_hemisphere(center_x, frame_width):
    """
    Determine if the center is in the left or right hemisphere
    """
    return 'A' if center_x < frame_width / 2 else 'B'

def post_transaction(class_id, movement):
    """
    Log the transaction in SQLite
    """
    cursor.execute(f'INSERT INTO transactions (class_id, movement) VALUES (?, ?)', (class_id, movement))
    conn.commit()

def main():
    # Create sqlite db if it doesn't exist
    create_db()

    model_path = os.getenv('BEST_MODEL_PATH')
    video_path = os.getenv('TEST_VIDEO_PATH')
    output_video_path = os.getenv('OUTPUT_VIDEO_PATH')

    model = load_model(model_path)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise FileNotFoundError(f"Video file {video_path} not found or cannot be opened.")

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    previous_positions = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame)

        predictions = []
        current_positions = {}

        for result in results:
            if len(result.boxes.xyxy) > 0 and result.boxes.conf[0].item() > 0.75:
                box = result.boxes.xyxy[0].tolist()
                class_id = result.names[result.boxes.cls[0].item()]
                confidence = result.boxes.conf[0].item()
                predictions.append({
                    'box': box,
                    'confidence': confidence,
                    'class': class_id
                })

                center_x = (box[0] + box[2]) / 2
                # center_y = (box[1] + box[3]) / 2 # Only needed if using quadrants

                current_positions[class_id] = get_hemisphere(center_x, frame_width)

        for class_id, current_hemisphere in current_positions.items():
            if class_id in previous_positions:
                prev_hemisphere = previous_positions[class_id]
                logging.info(f'Class ID: {class_id} -- Previous Hemisphere: {prev_hemisphere} -- Current Hemisphere: {current_hemisphere}')
                if prev_hemisphere != current_hemisphere:
                    if current_hemisphere == 'B':  # Left to Right
                        post_transaction(class_id, 1)
                        logging.info(f"Object '{class_id}' moved from {prev_hemisphere} to {current_hemisphere}. (+1 transaction logged)")
                    elif current_hemisphere == 'A':  # Right to Left
                        post_transaction(class_id, -1)
                        logging.info(f"Object '{class_id}' moved from {prev_hemisphere} to {current_hemisphere}. (-1 transaction logged)")

        # Update positions dictionary
        previous_positions.update(current_positions)


        
        # Annotate frame with predictions
        annotated_frame = display_predictions(frame, predictions)
        out.write(annotated_frame)

        # Optionally display the frame
        cv2.imshow("Smart Pantry Predictions", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    conn.close()

if __name__ == '__main__':
    main()
