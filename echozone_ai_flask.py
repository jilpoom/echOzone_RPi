from flask import Flask, request, redirect, jsonify, make_response
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras import layers, models
import os

app = Flask(__name__)



@app.route('/predict', methods = ['GET', 'POST'])
def load_predict():
    if request.method == 'POST':
        f = request.files['file']        
    f.save('./data/'+ secure_filename(f.filename))
    print("file upload")
    file = get_file_name()
    pre = (classify_model(resize_to_img(file)))
    # print(pre)
    # print("file delete") 
    
    os.remove(file)   
    #return redirect("http://localhost:8088/web/ai_test.do?pre={}".format(pre))
    return make_response(jsonify({"result" : pre}))
    
# 이미지 저장 함수
@app.route('/data_save', methods = ['GET', 'POST'])
def data_save():
    if request.method == 'POST':
        f = request.files['file']        
    f.save('./clean/'+ secure_filename(f.filename))
    #return redirect("http://www.naver.com")

# 이미지 폴더의 파일명 가져오는 합수
def get_file_name():
    data_path = './data'
    file_name_list = []
    for (root, directories, files) in os.walk(data_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name_list.append(file)
    # print(file_path)
    return file_path

# AI 예측하기
def classify_model(img):
    load_model = tf.keras.models.load_model('./ai_model/cup_class_epo100.h5') # 모델 불러오기
    pre = load_model.predict(img)
    if pre[0][0]<0.5:
        return 'dirty'
    else:
        return 'clean'

# 이미지 변환 함수
def img_to_array(img):
    return np.array(img, dtype = 'float32')/255.0

# 이미지 resize    
def resize_to_img(img):
    read_img = cv2.imread(img, cv2.COLOR_BGR2RGB)
    read_img = cv2.resize(read_img, (150, 150))
    read_img = img_to_array(read_img)
    img_array = [read_img]
    img_arr = np.array(img_array)
    img_arr.shape
    return img_arr    

@app.route('/test')
def naver_direct():
    pre = 1
    return redirect("http://localhost:8088/web/ai_test.do?pre={}".format(pre))

if __name__ == '__main__':
    app.run(host='172.20.10.10', debug=True, port=5050) 