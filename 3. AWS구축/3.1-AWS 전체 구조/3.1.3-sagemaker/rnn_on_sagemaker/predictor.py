# -*- coding: utf-8 -*-
import io
import sys
import json
import boto3
import os
import warnings
import tensorflow as tf

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

text = open('./onepiece_text.txt', 'rb').read().decode(encoding='utf-8')
weight_path = './onepiece_w.h5'

def make_model(text, weight_path, batch_size=256, embedding_dim = 256, rnn_units = 1024):
    vocab = sorted(set(text))
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(len(vocab), embedding_dim,
                                  batch_input_shape=[1, None]),
        tf.keras.layers.LSTM(rnn_units,
                            return_sequences=True,
                            stateful=True,
                            recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(len(vocab))])

    model.load_weights(weight_path)

    model.build(tf.TensorShape([1, None]))
    return model, char2idx, idx2char

model, char2idx,idx2char = make_model(text, weight_path)

def generate_text(start_string):
    num_generate = 200
    
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    text_generated = []

    temperature = 0.2

    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))




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

    input_word = data['word']

    print('Download finished!')
    # inference and send result to RDS and SQS

    print('Start to inference:')

    #make inference
    result_text = generate_text(start_string=u"{}".format(input_word))
    print(result_text)
    

    print("input_word:{},label:{}".format(input_word, result_text))
    print ("Done inference! ")
    inference_result = {
        'result_text':result_text
    }
    _payload = json.dumps(inference_result,ensure_ascii=False)


    return flask.Response(response=_payload, status=200, mimetype='application/json')
if __name__ == '__main__':
  app.run(host="127.0.0.1", port="5000")