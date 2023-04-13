
import sys
import os  
import shutil
import subprocess
import json 
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import numpy as np
import os
import tensorflow as tf
import pathlib 

#sagemaker data 
hyperparameters_file_path = "/opt/ml/input/config/hyperparameters.json"
inputdataconfig_file_path = "/opt/ml/input/config/inputdataconfig.json"
resource_file_path = "/opt/ml/input/config/resourceconfig.json"
data_files_path = "/opt/ml/input/data/"
failure_file_path = "/opt/ml/output/failure"
model_artifacts_path = "/opt/ml/model/"

from util import get_dataGenerator
import util

#path configuration 
def get_train_val_dirs(): 
    train_dir = os.path.join(data_files_path, 'train')
    test_dir = os.path.join(data_files_path, 'test')
    validation_dir = os.path.join(data_files_path, 'validation')

    train_dir = pathlib.Path(train_dir)
    test_dir = pathlib.Path(test_dir)
    validation_dir = pathlib.Path(validation_dir)
    return train_dir, test_dir, validation_dir


import tarfile 
import shutil 
def train():
    train_dir, test_dir, validation_dir = get_train_val_dirs()
    train_generator, test_generator, validation_generator = get_dataGenerator(train_dir, test_dir, validation_dir)

    model = util.get_model()

    model.compile(loss = 'categorical_crossentropy',
    optimizer = optimizers.RMSprop(lr=1e-4),
    metrics=['accuracy'])

    initial_epochs = 50
    history = model.fit(train_generator,
                    epochs=initial_epochs,
                    validation_data=validation_generator)
    model.save('./tlmodel') 
    tar = tarfile.open("tlmodel.tar.gz", "w:gz")
    tar.add("./tlmodel", arcname="tlmodel")
    tar.close() 
    shutil.move("tlmodel.tar.gz", model_artifacts_path)
    

if __name__ == "__main__":
    train()
