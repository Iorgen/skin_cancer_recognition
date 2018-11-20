import numpy as np
import pandas as pd
import os 
import torch.utils.data as data
import keras
import random 
import itertools
from keras import models
from keras import layers
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Conv1D

from keras.preprocessing import image
from numpy import array
from keras import metrics
from PIL import Image
from keras.preprocessing.image import img_to_array,array_to_img, load_img
from keras.utils import to_categorical
import tensorflow as tf
import cv2

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import numpy as np
import pandas as pd
import os
from glob import glob
import seaborn as sns
base_skin_dir = os.path.join('', 'dataset')

import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler



def load_img_with_cv2(imagePath):
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    image = img_to_array(image)
    return image

def load_image(imagePath):
    image = cv2.imread(imagePath)
    return image

def add_gray_channel_to_image(image):
    


if __name__ == '__main__':
    data = []
    IMAGE_DIMS = (100, 75, 3)
    lesion_type_dict = {
        'nv': 'Melanocytic nevi',
        'mel': 'dermatofibroma',
        'bkl': 'Benign keratosis-like lesions ',
        'bcc': 'Basal cell carcinoma',
        'akiec': 'Actinic keratoses',
        'vasc': 'Vascular lesions',
        'df': 'Dermatofibroma'}
    imageid_path_dict = {os.path.splitext(os.path.basename(x))[0]: x for x in glob(os.path.join(base_skin_dir, '*', '*.jpg'))}
    skin_data = pd.read_csv(os.path.join(base_skin_dir, 'HAM10000_metadata.csv'))
    skin_data['path'] = skin_data['image_id'].map(imageid_path_dict.get)
    skin_data['cell_type'] = skin_data['dx'].map(lesion_type_dict.get) 
    skin_data['cell_type_idx'] = pd.Categorical(skin_data['cell_type']).codes
    IMG = load_img_with_cv2(skin_data['path'][0])

    print('it is working')



