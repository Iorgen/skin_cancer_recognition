import cv2
import numpy as np
import pandas as pd
IMAGE_DIMS = (60, 45, 3)
from keras.preprocessing.image import img_to_array,array_to_img, load_img


def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.resize(hsv, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img_to_array(img)
    return img


# return thresholding featrue transformation
def thresholding_feature(imagePath):
    img_grey = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    img_grey = cv2.resize(img_grey, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    # # Adaptive Gaussian
    img_grey = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img_grey, (3, 3), 0)
    ret3, img_binary = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # invert black = 255
    # ret, thresh1 = cv2.threshold(img_binary, 157, 255, cv2.THRESH_BINARY_INV)
    img_binary = img_to_array(img_binary)
    return img_binary


def load_atm_img(imagePath):
    img = cv2.imread(imagePath, 0)
    img = cv2.resize(img, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    atm_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # TODO make it gray
    atm_img = img_to_array(atm_img)
    return atm_img


def load_img_with_cv2(imagePath, frth_channel='without'):
    channel = False
    image = load_img(imagePath)
    sub_channel = 'no_channel'
    if frth_channel == 'atm':
        sub_channel = load_atm_img(imagePath)
        channel = True
    elif frth_channel == 'gray':
        sub_channel = increase_brightness(image, 150)
        channel = True
    elif frth_channel == 'threshold':
        sub_channel = thresholding_feature(imagePath)
        channel = True
    image = img_to_array(image)
    if channel == True:
        multiImage = np.concatenate((image, sub_channel), axis=2)
        return multiImage
    else:
        return image


def load_gray(imagePath):
    image = load_img(imagePath)
    return increase_brightness(image, 150)