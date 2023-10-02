# **Deep-learning-Cortaderia-selloana**

This data/code was developed and used in the context of the research article: (_Can citizen-science and social media images support the early detection of new invasion sites? A deep learning test case with Cortaderia selloana_; Ana Sofia Cardoso, Eva Malta-Pinto, Siham Tabik, Tom August, Helen E. Roy, Ricardo Correia, Joana R. Vicente, Ana Sofia Vaz; Ecological Informatics, doi).

This project was implemented using nine different pre-trained convolutional neural network architectures (VGG16, ResNet50, ResNet101, Inception-v3, DenseNet201, EfficientNetB0, Faster R-CNN ResNet50, Faster R-CNN ResNet101 and Faster R-CNN Inception-v2), depending on the pretended task (classification or object detection), along with three different weights (ImageNet, MSCOCO and iNaturalist).

We started collecting citizen-science and social media images using the extract_images_by_url.py and extract_fickr_images.py scripts. Then, we manually labelled each image according to the selected task (classification or object detection), which results can be found in the Labels_cortaderia_citizenscience.xlsx and Labels_cortaderia_socialmedia.xlsx files, for the classification task, and label_map.pbtxt, train.record and test.record, for the object detection task. The images and the train.record file can be found at Zenodo (https://doi.org/10.5281/zenodo.8393518).

Regarding the training of the convolutional neural network models, we started developing the classification task, that can be implemented using the classification_cortaderia.py script, followed by the object detection task, which in turn can be performed using the object_detection_cortaderia.py script. For the object detection task it's necessary to provide a configuration file, depending on the architecture selected, that can be found in the Configurations folder.

To test the generalization and transferability capacity of the networks, we also feeded the saved models with new and unseen social media images, using the socialmedia.record and Social_media_dataset.zip files that can be found at Zenodo (https://doi.org/10.5281/zenodo.8393518).

In the script files is only represented the DenseNet201 architecture with ImageNet weights, for the classification task, and the Faster R-CNN ResNet101 architecture with MS COCO weights, for the object detection task, as these two pairs achieved the best results for our project. All analyzes were performed using the free T4 GPU environment provided by Google Colab.
