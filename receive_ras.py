import argparse

import numpy as np
from werkzeug.utils import secure_filename
import cv2
from flask import Flask, Response, request, session, render_template,redirect
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)
app.secret_key = "hello"

# app.config['MONGO_DBNAME']='NCKH'
app.config['MONGO_URI']='mongodb+srv://thinhz:123@testdb.ah0wxda.mongodb.net/test1'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 # tăng session size

mongo = PyMongo(app)

def gen_normal():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (0, 0), fx=1.0, fy=1.0)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # time.sleep(0.1)
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

@app.route('/api/loadimage', methods=['GET', 'POST'])
def loadimage():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # if request.method == 'POST':
    #     data1 = {'message': 'size={}x{}'.format(img.shape[1], img.shape[0])}
    #     mongo.db.infor.insert_one(data1)
    #     session['img'] = img.tolist()
    #     return 'receive image'
    # else:
    #     img_list = session.get('img', None)
    #     if img_list is not None:
    #         img = np.array(img_list)
    #         img_response = Response(response=img.tobytes(), status=200, mimetype='image/jpeg')
    #         return img_response
    #     else:
    #         return 'No image in session'
    # # response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    # response_pickled = jsonpickle.encode(response)
    # return Response(response=response_pickled, status=200, mimetype="application/json")
    session['image'] = img.tolist()
    return redirect('/display')

@app.route('/upload', methods=['POST'])
def upload():
    # file = request.files['file']
    # image_data = file.read()
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    session['image'] = img.tolist()
    return 'Image uploaded!'

@app.route('/display')
def display():
    image_data = session.get('image', None)
    if image_data is None:
        return 'No image uploaded!'
    else:
        # create a temporary file path
        img = np.array(image_data)
        tmp_path = '/test/anh_test.jpg'
        with open(tmp_path, 'wb') as f:
            f.write(img)
        # render template with img tag that references temporary file path
        return render_template('upload.html', image_path=tmp_path)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src  attributeof an img tag."""
    return Response(gen_normal(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def hello():
    return "hello"

# @app.route('/testMongo')
# def index():
#     user_colllection = mongo.db.infor
#     user_colllection.insert_one({'name': 'duc'})
#     return 'add ok'

##################################
if __name__ == ("__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        default=5000, help="Running port")
    parser.add_argument("-H", "--host", type=str,
                        default='0.0.0.0', help="Address to broadcast")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True)