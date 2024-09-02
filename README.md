# smart_pantry_model

## YOLO Model
With respect to YOLOv8, the 'imgsz' parameter during model training allows for flexible input sizes. When set to a specific size, such as 640, the model will resize input images so their largest dimension is 640 pixels while maintaining the original aspect ratio.

By evaluating your model's and dataset's specific needs, you can determine whether resizing is a necessary preprocessing step or if your model can efficiently handle images of varying sizes.

With respect to YOLOv8, normalization is seamlessly handled as part of its preprocessing pipeline during model training. YOLOv8 automatically performs several preprocessing steps, including conversion to RGB, scaling pixel values to the range [0, 1], and normalization using predefined mean and standard deviation values.

Original Data requires processing. Run the following scripts currently.

## NCNN
Key Features of NCNN Models
NCNN models offer a wide range of key features that enable on-device machine learning by helping developers run their models on mobile, embedded, and edge devices:

- Efficient and High-Performance: NCNN models are made to be efficient and lightweight, optimized for running on mobile and embedded devices like Raspberry Pi with limited resources. They can also achieve high performance with high accuracy on various computer vision-based tasks.

- Quantization: NCNN models often support quantization which is a technique that reduces the precision of the model's weights and activations. This leads to further improvements in performance and reduces memory footprint.

- Compatibility: NCNN models are compatible with popular deep learning frameworks like TensorFlow, Caffe, and ONNX. This compatibility allows developers to use existing models and workflows easily.

- Easy to Use: NCNN models are designed for easy integration into various applications, thanks to their compatibility with popular deep learning frameworks. Additionally, NCNN offers user-friendly tools for converting models between different formats, ensuring smooth interoperability across the development landscape.


Run:
- delete_img_label_files.py: Deletes the classes that do not fit the classification model from a particular dataset
- create_data_yaml.py: Creates the final models data.yaml file with relative train and test paths and classes from a unique set of all the data.yaml files in the data dir
- update_labels.py: Updates the labels in the label files for all labels in the data directory to the new data.yaml. It then copies the files to yolo model directory.
- update_images.py: Moves the images to the final image directory in yolo models
- random_split.py: Randomly splits the images into 70:20:10 for train:test:valid respect

or 

./start.sh
