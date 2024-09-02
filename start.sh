#!/bin/bash
python scripts/create_new_data_yaml.py &&
python scripts/update_labels.py &&
python scripts/update_images.py &&
python scripts/random_split.py 

