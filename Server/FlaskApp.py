from flask import Flask, request, render_template, redirect, url_for, json, Response, jsonify
from werkzeug.utils import secure_filename
from keras import backend as K
import numpy as np
import os
# import augmentation
import keras
from keras.models import Model
import pandas as pd
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.optimizers import Adam
from keras import models
from keras import layers
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Conv1D
import cv2
optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
UPLOAD_FOLDER = 'upload_img'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_model():
    model = models.Sequential()
    model.add(layers.Conv2D(64, (3, 3), input_shape=(100, 75, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(64, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(128, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(128, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(256))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(4))
    model.add(layers.Activation('sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    return model


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route('/')
def main_page():
    return render_template('FrontEnd/index.html')


@app.route('/image-recog', methods=['GET','POST'])
def check_image():
    if request.method == 'POST' and request.files['file']:  # this block is only entered when the form is submitted
        # Get file name and save file to disk
        img_file = request.files['file']
        filename = secure_filename(img_file.filename)
        img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # resize image adn convert it to numpy.ndarray
        image = cv2.imread(UPLOAD_FOLDER + "/" + filename, cv2.IMREAD_UNCHANGED)
        image = cv2.resize(image, (75, 100))
        image = img_to_array(image)
        pred_image = image.reshape(1, 100, 75, 3)

        # Create CNN model and load weights for it
        model = create_model()
        model.load_weights('weights.h5')

        # make a prediction based on loaded photo
        hist = model.predict(pred_image)
        K.clear_session()
        data = {
            'name': "John",
            'surname': "Vagner",
            'diag': "Melanoma",
            'shape': hist.tolist()
        }
        # pack prediction result in JSON
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://luisrei.com'
        return resp
    else:
        return not_found()

if __name__ == '__main__':
    app.run()

