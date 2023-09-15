import os

os.chdir('/content/Tensorflow/models/research') #from https://github.com/tensorflow/models.git
protoc object_detection/protos/*.proto --python_out=.

os.chdir('/content/Tensorflow/models/research/slim') #from https://github.com/tensorflow/models.git
python setup.py build
python setup.py install
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

import os
os.chdir('/content/Tensorflow/models/research/object_detection/') #from https://github.com/tensorflow/models.git

#train the model
python model_main.py --logtostderr --model_dir=resnet101cocot0 --pipeline_config_path=resnet101cocot0/resnet101_coco.config #when using the Faster R-CNN ResNet101

#evaluate the model
python model_main.py --alsologtostderr --run_once --checkpoint_dir= resnet101cocot0 --model_dir= resnet101cocot0/eval/ --pipeline_config_path= resnet101cocot0/resnet101_coco.config #when using the Faster R-CNN ResNet101

#test the model with a new dataset of images
python legacy/eval.py --logtostderr --pipeline_config_path= resnet101cocot0/resnet101_coco.config --checkpoint_dir= resnet101cocot0 --eval_dir= resnet101cocot0/eval #when using the Faster R-CNN ResNet101
