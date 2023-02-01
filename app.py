# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

# v4l2-ctl --list-devices # WEBCAM check
# chmod 777 /dev/video

# python
import cv2
from PIL import Image
from io import BytesIO
from flask import Flask, Response, send_file, redirect, url_for, render_template, make_response, jsonify
import requests
from CameraService import CameraService
from pyzbar import pyzbar
import threading
import time
from flask_cors import CORS



# RPi GPIO setting
import CupDetectionUltrasonic as CupDetect
import CupEntrance

import RPi.GPIO as GPIO



save_path = 'recode'

# QR code global variable
global BARCODE_DATA 
global USER_CHECK
BARCODE_DATA = -1
USER_CHECK = False


# current app name
app = Flask(__name__)
with app.app_context():
    print(app.name)
    CORS(app)
    

cap = CameraService(0)
cap.start();


# QR_Code redbox in CameraRead
def QR_box(imgRGB):
    box_color = (255, 0, 0)
    imgRGB = cv2.rectangle(imgRGB, (160, 80), (480, 400), box_color, 3)
    return imgRGB

# Cup_box in Camera display

# main 
@app.route("/")
def hello_world(): 
    return render_template('index.html')



def cameraRead(camera):
    while True:
        frame = camera.read()
        if frame is not None:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      
            jpg = Image.fromarray(imgRGB)
            content = BytesIO()
            jpg.save(content, 'JPEG')
            
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + content.getvalue() + b'\r\n')
          
                    
# QR_code Detect and camera frame yield
def QR_Read(camera):
    global BARCODE_DATA
    global USER_CHECK
    

    
    while True:
        frame = cap.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgRGB = QR_box(imgRGB)
        jpg = Image.fromarray(imgRGB)
        barcodes = pyzbar.decode(imgRGB[160:480, 80:400])
            
        if len(barcodes) != 0:
            for barcode in barcodes:
                BARCODE_DATA = barcode.data.decode('utf-8')
                USER_CHECK = is_user_QR(BARCODE_DATA)
        jpg = Image.fromarray(imgRGB)
        content = BytesIO()
        jpg.save(content, 'JPEG')        
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + content.getvalue() + b'\r\n')
        
        

            
# Camera source url
@app.route('/stream.mjpg')
def stream():
    response = Response(cameraRead(cap),
                        mimetype='multipart/x-mixed-replace; boundary=frame')       
    return response


def is_user_QR(data):

    user_Check = False
    if 0 <= int(data) <= 100:
        user_Check = True
        return user_Check
    
    

# QR code data responsebody
@app.route('/DataSend', methods=['POST'])
def DataSend():
    global USER_CHECK
    global BARCODE_DATA    
    
    data = {'userCheck' : str(USER_CHECK),
            'userData' : BARCODE_DATA
            }
    
    return make_response(jsonify(data))   


@app.route('/DataSetting', methods=['POST'])
def DataSetting():
    global USER_CHECK 
    global BARCODE_DATA

    USER_CHECK = False
    BARCODE_DATA = -1
    
    
    return make_response(jsonify({'Settings' : 'Success' }))



@app.route('/QR')    
@app.route('/QR_stream.mjpg')
def QR_stream():
        
    response = Response(QR_Read(cap),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    
    return response
    




@app.route('/recode/<name>')
def recode(name):
    cap.recode(f'{name}.mp4')
    return ('', 204)

@app.route('/save')
def save():
    cap.save()
    return ('', 204)

@app.route('/download/<name>')
def download(name):
    return send_file(f'{save_path}/{name}.mp4', as_attachment=True)

@app.route('/snapshot')
def snapshot():
    frame = cap.read()
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    jpg = Image.fromarray(imgRGB)
    content = BytesIO()
    jpg.save(content, 'JPEG')
    return Response(content.getvalue(), mimetype='image/jpeg')

# camera frame capture and send to machine learning model
@app.route('/predict', methods=['POST'])
def predict():
    cupCheck = CupDetect.isCupDetect()
    cnt = 0;
        
    if cupCheck :
        frame = cap.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        jpg = Image.fromarray(imgRGB)
        jpg.save('image.jpg')
            
        file = open('image.jpg', 'rb')
        data = {'file' : file}
            
        url = "http://172.20.10.10:5050/predict"
            
        predict_result = requests.post(url, files=data).json()
        
        if predict_result['result'] == 'clean':
            thread_motorOpen = threading.Thread(target=CupEntrance.motorOpen)
            thread_motorOpen.daemon = True
            thread_motorOpen.start()
                
            return make_response(jsonify({'result' : 'clean'}))
        
        else:
            return make_response(jsonify({'result' : 'dirty'}))
        
        


if __name__ == '__main__':
    app.run(host='172.20.10.13', threaded=True)
    