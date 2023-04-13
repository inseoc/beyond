# -*- coding: utf-8 -*-
import io
import sys
import json
import boto3
import os
import warnings

warnings.filterwarnings("ignore",category=FutureWarning)

sys.path.append('/opt/program/textrank4zh')

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    # from autogluon import ImageClassification as task

import flask
from tensorflow.keras import models
from PIL import Image
import numpy as np

# dataset의 종류 리스트
print(os.getcwd())
model_cloth = models.load_model('./clothes.h5')
model_color = models.load_model('./color.h5')

def get_cloth(image):

    # 이미지 resize
    decode_img = io.BytesIO(image)
    img = Image.open(decode_img)
    img = img.convert("RGB")
    img = img.resize((150,150))
    data = np.asarray(img)

    X = np.array(data)
    X = X.astype("float") / 255
    X = X.reshape(-1, 150, 150,3)

    # 예측
    pred = model_cloth.predict(X)  
    result = np.argmax(pred)   # 예측 값중 가장 높은 클래스 반환
    # cloth = cloth_list[result]    # 한글로 반환

    return result

def get_color(image):

    # 이미지 resize
    decode_img = io.BytesIO(image)
    img = Image.open(decode_img)
    img = img.convert("RGB")
    img = img.resize((150,150))
    data = np.asarray(img)

    X = np.array(data)
    X = X.astype("float") / 255
    X = X.reshape(-1, 150, 150,3)

    # 예측
    pred = model_color.predict(X)  
    result = np.argmax(pred)   # 예측 값중 가장 높은 클래스 반환
    # color = color_list[result]    # 한글로 반환

    return result


# The flask app for serving predictions
app = flask.Flask(__name__)

s3 = boto3.client('s3')

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    # health = ScoringService.get_model() is not None  # You can insert a health check here
    health = 1

    status = 200 if health else 404
    print("===================== PING ===================")
    return flask.Response(response="{'status': 'Healthy'}\n", status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def invocations():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    print("================ INVOCATIONS =================")

    #parse json in request
    print ("<<<< flask.request.content_type", flask.request.content_type)

    data = flask.request.data.decode('utf-8')
    data = json.loads(data)

    bucket = data['bucket']
    image_uri = data['image_uri']

    download_file_name = image_uri.split('/')[-1]
    print ("<<<<download_file_name ", download_file_name)

    print (image_uri)
    file_obj = s3.get_object(Bucket=bucket, Key=image_uri)
    file_obj = file_obj["Body"].read()
    # s3_client.get_object(bucket, image_uri, download_file_name)
    #local test
    # download_file_name='./test_baji.jpg'
    print('Download finished!')
    # inference and send result to RDS and SQS

    print('Start to inference:')

    #LOAD MODEL
    model_cloth = './clothes.h5'
    model_color = './color.h5'

    #make inference
    cloth = int(get_cloth(file_obj))
    color = int(get_color(file_obj))
    print("image_path:{},label:{},label2:{}".format(image_uri, cloth, color))
    print ("Done inference! ")
    inference_result = {
        'cloth':cloth,
        'color':color
    }
    _payload = json.dumps(inference_result,ensure_ascii=False)


    return flask.Response(response=_payload, status=200, mimetype='application/json')
if __name__ == '__main__':
  app.run(host="127.0.0.1", port="5000")