from ultralytics import YOLO

from dotenv import load_dotenv
import os

load_dotenv()

model_path = os.getenv('BEST_MODEL_PATH')

model = YOLO(model_path)

# Export the model to NCNN format
model.export(format="ncnn")  

# # Load the exported NCNN model
# ncnn_model = YOLO("./yolov8n_ncnn_model")

