from ultralytics import YOLO
from dotenv import load_dotenv
import os
import torch

# Load environment variables
load_dotenv(dotenv_path='.env.yolo')
data_yaml = os.getenv('YOLO_YAML')
model_path = os.getenv('MODEL_PATH')
finished_model_path = os.getenv('FINISHED_MODEL')

def train_model():
    """
    Train the YOLO model from scratch or using pretrained weights.
    """
    # Load pretrained model
    model = YOLO(model_path)  
    
    # Start training
    results = model.train(
        data=data_yaml, 
        epochs=250, 
        patience=25
    )

def resume_training():
    """
    Resume training from the last checkpoint.
    """
    # Check if the checkpoint exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Checkpoint not found at: {model_path}")
    
    # Load model and handle any issues with optimizer state
    model = YOLO(model_path)
    
    # Try to resume training, handle optimizer state issues
    try:
        results = model.train(resume=model_path, data=data_yaml, epochs=100, patience=25)
    except KeyError as e:
        print(f"KeyError encountered: {e}. Removing optimizer state and trying again.")
        
        # Load the checkpoint
        ckpt = torch.load(model_path)
        
        # Remove the optimizer state
        if 'optimizer' in ckpt:
            del ckpt['optimizer']
        
        # Save the modified checkpoint back
        torch.save(ckpt, model_path)
        print("Checkpoint saved without optimizer state.")
        
        # Retry training after removing optimizer state
        model = YOLO(model_path)
        results = model.train(resume=model_path, data=data_yaml, epochs=100, patience=25)
    
    # Save results or handle as needed
    print("Training resumed successfully.")

def continue_training(additional_epochs=50):
    """
    Continue training for an additional number of epochs after resuming from a checkpoint.
    
    Args:
        additional_epochs (int): Number of additional epochs to train.
    """
    # Check if the checkpoint exists
    if not os.path.exists(finished_model_path):
        raise FileNotFoundError(f"Checkpoint not found at: {model_path}")
    
    # Load model and handle any issues with optimizer state
    model = YOLO(finished_model_path)
    
    # Continue training for the specified number of additional epochs
    print(f"Continuing training for {additional_epochs} more epochs...")
    results = model.train(data=data_yaml, epochs=additional_epochs, patience=25)
    
    # Save results or handle as needed
    print(f"Training continued for additional {additional_epochs} epochs successfully.")


def main():
    # Call the appropriate function to either train or resume training
    continue_training()

if __name__ == '__main__':
    main()
