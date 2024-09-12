

from ultralytics import YOLO
from dotenv import load_dotenv
import os

# Environment variables
load_dotenv(dotenv_path='.env.yolo')
data_yaml = os.getenv('YOLO_YAML')
MODEL_PATH = os.getenv('YOLO_MODEL')



def resume_training():
    model = YOLO(MODEL_PATH)

    results = model.train(
        data=data_yaml,      # The path to your rebalanced dataset
        epochs=100,            # Number of epochs for transfer learning
        learning_rate=0.001,   # Lower learning rate for fine-tuning
        resume=True,           # Continue from the previous best checkpoint
        patience=20            # Early stopping patience
    )

def main():
    resume_training()

if __name__ == '__main__':
    main()
