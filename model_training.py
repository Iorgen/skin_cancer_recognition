from neuro_topology import *
from image_preproccesing import *
import json
from keras.preprocessing.image import img_to_array,array_to_img, load_img
from keras import backend as K
from keras.optimizers import Adam, RMSprop,SGD
import tensorflow as tf
import cv2
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import os
from glob import glob
base_skin_dir = os.path.join('', 'dataset')


lesion_type_dict = {
    'nv': 'Melanocytic nevi',
    'mel': 'dermatofibroma',
    'bkl': 'Benign keratosis-like lesions ',
    'bcc': 'Basal cell carcinoma',
    'akiec': 'Actinic keratoses',
    'vasc': 'Vascular lesions',
    'df': 'Dermatofibroma'
}


# default loading
def load_img(imagePath):
    image = cv2.imread(imagePath, cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
    image = img_to_array(image)
    return image


def f1(y_true, y_pred):
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.is_nan(f1), tf.zeros_like(f1), f1)
    return K.mean(f1)


if __name__ == '__main__':
    print('START')
    imageid_path_dict = {os.path.splitext(os.path.basename(x))[0]: x
                         for x in glob(os.path.join(base_skin_dir, '*', '*.jpg'))}
    skin_data = pd.read_csv(os.path.join(base_skin_dir, 'HAM10000_metadata.csv'))
    skin_data['path'] = skin_data['image_id'].map(imageid_path_dict.get)
    skin_data['cell_type'] = skin_data['dx'].map(lesion_type_dict.get)
    skin_data['cell_type_idx'] = pd.Categorical(skin_data['cell_type']).codes
    skin_data['dx'].value_counts()
    current_skin_data = skin_data
    print(current_skin_data.dx.value_counts())
    # load baseline data
    data = []
    for img_path in current_skin_data['path']:
        data.append(load_img_with_cv2(img_path))
    labels = np.array(current_skin_data['dx'])
    # load generate image data
    generate_data = []
    generate_labels = []
    # for loop from dx from skin cancer recognition
    for dx in current_skin_data['dx'].unique():
        path_dir = 'generate_img/' + dx + '/*.jpeg'
        for filename in glob(path_dir):
            img = load_img_with_cv2(filename)
            generate_data.append(img)
            generate_labels.append(dx)
    print('изображения загружены')
    #  Splitting into test and training samples
    x_train, x_test, y_train, y_test = train_test_split(
        data, labels, test_size=0.2, random_state=42)
    # normalization baseline data
    x_test_mean = np.mean(x_test)
    x_test_std = np.std(x_test)
    x_test = (x_test - x_test_mean) / x_test_std
    # connect baseline dataset and generating dataset
    generate_labels = np.array(generate_labels)
    full_labels = np.concatenate((y_train, generate_labels))
    generate_data = np.array(generate_data, dtype=np.uint8)
    full_data = np.concatenate((x_train, generate_data))
    # data normalization
    full_data_mean = np.mean(full_data)
    full_data_std = np.std(full_data)
    full_data = (full_data - full_data_mean) / full_data_std
    print('Данные нормализованы')
    # one hot encoding data
    mlb = LabelBinarizer()
    full_labels = mlb.fit_transform(full_labels)
    y_test = mlb.fit_transform(y_test)
    # splitting into test and validation samples
    x_train, x_validate, y_train, y_validate = train_test_split(full_data, full_labels,test_size=0.1, random_state=2)
    OPT = task_optimizer('Adam')
    NNW = topology_d(OPT)
    print('learning was started')
    history = NNW.fit(x_train, y_train, epochs=1, batch_size=64, validation_data=(x_validate, y_validate))
    with open('trainnig_history.json', 'w') as f:
        json.dump(history.history, f)
    loss, accuracy = NNW.evaluate(x_test, y_test, verbose=1)
    loss_v, accuracy_v = NNW.evaluate(x_validate, y_validate, verbose=1)
    print("Validation: accuracy = %f  ;  loss = %f  " % (accuracy_v, loss_v))
    print("Test: accuracy = %f  ;  loss = %f ;" % (accuracy, loss))
    # model.save_weights("weights.h5")
    # print("Saved model to disk")
