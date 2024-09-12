#!/bin/bash

echo "Running create_new_data_yaml.py..."
python scripts/create_new_data_yaml.py &&
echo "Finished create_new_data_yaml.py. Running update_labels.py..." &&
echo "---------------------------------------------" &&
python scripts/update_labels.py &&
echo "Finished update_labels.py. Running update_images.py..." &&
echo "---------------------------------------------" &&
python scripts/update_images.py &&
echo "Finished update_images.py."

