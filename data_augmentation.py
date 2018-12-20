import os
from glob import glob
base_skin_dir = os.path.join('', 'dataset')
import pandas as pd
import os
from keras.preprocessing.image import img_to_array,array_to_img, load_img
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

lesion_type_dict = {
    'nv': 'Melanocytic nevi',
    'mel': 'dermatofibroma',
    'bkl': 'Benign keratosis-like lesions ',
    'bcc': 'Basal cell carcinoma',
    'akiec': 'Actinic keratoses',
    'vasc': 'Vascular lesions',
    'df': 'Dermatofibroma'
}

datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')


def img_augmentation(data, dx_condition, count_for_creating):
    aug_data = data[current_skin_data['dx'] == dx_condition]
    aug_data.head()
    print(aug_data.empty)
    if aug_data.empty == False:
        print('it is in for')
        for path in aug_data['path']:
            img = load_img(path)
            x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
            x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
            i = 0
            save_path = 'generate_img/' + dx_condition
            for batch in datagen.flow(x, batch_size=1,
                          save_to_dir=save_path, save_prefix=dx_condition, save_format='jpeg'):
                i += 1
                if i > count_for_creating:
                    break  # otherwise the generator would loop indefinitely


if __name__ == '__main__':
    imageid_path_dict = {os.path.splitext(os.path.basename(x))[0]: x
                         for x in glob(os.path.join(base_skin_dir, '*', '*.jpg'))}
    skin_data = pd.read_csv(os.path.join(base_skin_dir, 'HAM10000_metadata.csv'))
    skin_data['path'] = skin_data['image_id'].map(imageid_path_dict.get)
    skin_data['cell_type'] = skin_data['dx'].map(lesion_type_dict.get)
    skin_data['cell_type_idx'] = pd.Categorical(skin_data['cell_type']).codes
    skin_data['dx'].value_counts()
    current_skin_data = skin_data
    current_skin_data.dx.value_counts()
    img_augmentation(current_skin_data, 'akiec', 12)
    img_augmentation(current_skin_data, 'bcc', 8)
    img_augmentation(current_skin_data, 'bkl', 5)
    img_augmentation(current_skin_data, 'df', 30)
    img_augmentation(current_skin_data, 'mel', 5)
    img_augmentation(current_skin_data, 'vasc', 26)
