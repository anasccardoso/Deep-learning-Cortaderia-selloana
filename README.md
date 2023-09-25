# Deep-learning-Cortaderia-selloana

This project was implemented using nine different pre-trained convolutional neural network architectures (VGG16, ResNet50, ResNet101, Inception-v3, DenseNet201, EfficientNetB0, Faster R-CNN ResNet50, Faster R-CNN ResNet101 and Faster R-CNN Inception-v2), depending on the pretended task (classification or object detection), along with three different weights (ImageNet, MSCOCO and iNaturalist).

We started collecting citizen-science and social media images through the extract_images_by_url.py and extract_fickr_images.py scripts. Then, we manually labelled each image according to the selected task (classification or object detection), which results can be found in the Labels_cortaderia_citizenscience.xlsx and Labels_cortaderia_socialmedia.xlsx files, for the classification task, and label_map.pbtxt, train.record and test.record, for the object detection task. The images and the train.record file can be found at Zenodo (https://doi.org/10.5281/zenodo.8348734).

In the script files is only represented the DenseNet201 architecture with ImageNet weights, for the classification task, and the Faster R-CNN ResNet101 architecture with MS COCO weights, for the object detection task, as these two pairs achieved the best results for our project. All analyzes were performed using the free T4 GPU environment provided by Google Colab.
