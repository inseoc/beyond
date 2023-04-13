# -*- coding: utf-8 -*-
import io
import sys
import json
import boto3
import os
import warnings
import transformer

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

# The flask app for serving predictions
app = flask.Flask(__name__)

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

    category = data['category']
    color = data['color']
    size = data['size']
    washing = data['washing']

    request_text = category + "," + color + "," + size + "," + washing

    print('Start to inference:')

    # predict("레이어트뷔스티에 원피스,베이지,M,손세탁,드라이")
    result_text = transformer.predict(request_text)

    #make inference
    print("inferenced text:{}".format(result_text))
    print ("Done inference! ")
    inference_result = {
        'result_text':result_text
    }
    _payload = json.dumps(inference_result,ensure_ascii=False)


    return flask.Response(response=_payload, status=200, mimetype='application/json')
if __name__ == '__main__':
  app.run(host="127.0.0.1", port="5000")