from flask import Flask, request, render_template, redirect, url_for, json, Response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
UPLOAD_FOLDER = 'upload_img'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        # TODO: save file on folder
        # TODO: load model from joson
        # TODO: Model.predict by image
        data = request.files['file']
        filename = secure_filename(data.filename)
        data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = {
            'name': data.filename,
            'surname': "Vagner",
            'diag': "Melanoma"
        }
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://luisrei.com'
        return resp
        # # read image file string data
        # filestr = request.files['file'].read()
        # # convert string data to numpy array
        # npimg = numpy.fromstring(filestr, numpy.uint8)
        # # convert numpy array to image
        # img = cv2.imdecode(npimg, cv2.CV_LOAD_IMAGE_UNCHANGED)
    else:
        return not_found()

if __name__ == '__main__':
    app.run()

