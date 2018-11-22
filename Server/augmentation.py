import cv2
import os
import keras
import random
import itertools
import os
import tensorflow as tf
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
from keras import models
from keras import layers
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Conv1D
from numpy import array
from keras import metrics
from keras.preprocessing.image import img_to_array, array_to_img, load_img
from keras.utils import to_categorical
from glob import glob
base_skin_dir = os.path.join('', 'dataset')

# cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
# cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
# cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel

def hello():
    return 'Hello_world'

# return image with higher increase brightness
def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

# return thresholding featrue transformation
def thresholding_feature(imagePath):
    Image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    img_grey = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    # # Adaptive Gaussian
    img_grey = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img_grey, (3, 3), 0)
    ret3, img_binary = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # invert black = 255
    # ret, thresh1 = cv2.threshold(img_binary, 157, 255, cv2.THRESH_BINARY_INV)
    return img_binary 

def load_data():
    imageid_path_dict = {os.path.splitext(os.path.basename(x))[0]: x for x in glob(os.path.join(base_skin_dir, '*', '*.jpg'))}
    lesion_type_dict = {
        'nv': 'Melanocytic nevi',
        'mel': 'dermatofibroma',    
        'bkl': 'Benign keratosis-like lesions ',
        'bcc': 'Basal cell carcinoma',
        'akiec': 'Actinic keratoses',
        'vasc': 'Vascular lesions',
        'df': 'Dermatofibroma'
    }
    skin_data = pd.read_csv(os.path.join(
        base_skin_dir, 'HAM10000_metadata.csv'))
    skin_data['path'] = skin_data['image_id'].map(imageid_path_dict.get)    
    skin_data['cell_type'] = skin_data['dx'].map(lesion_type_dict.get)
    skin_data['cell_type_idx'] = pd.Categorical(skin_data['cell_type']).codes
    skin_data['dx'].value_counts()
    return skin_data

if __name__ == '__main__':
    IMAGE_DIMS = (100, 75, 3)
    skin_data = load_data()
    watching_skin_path = skin_data['path'][25]
    thr = thresholding_feature('dataset\\images_part_1\\ISIC_0024684.jpg')
    # Image = cv2.imread('dataset\\images_part_1\\ISIC_0024684.jpg', cv2.IMREAD_UNCHANGED)
    # thr = increase_brightness(Image,value=150)
    print(len(thr.shape))
    cv2.imshow('image', thr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
