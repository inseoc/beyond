
import os 
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import VGG16
import numpy as np 

BATCH_SIZE = 32
IMG_SIZE = (224, 224)
CHANNELS = 3
AUTOTUNE = tf.data.experimental.AUTOTUNE
class_names = [] 
def get_model():
    conv_base = VGG16(weights='imagenet',
    include_top=False,
    input_shape=(IMG_SIZE[0],IMG_SIZE[0],CHANNELS))

    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(256, activation='relu'))

    model.add(layers.Dense(12, activation='softmax'))
    conv_base.trainable = False

    return model 

def get_dataGenerator(train_dir, test_dir, validation_dir):
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    datagen = ImageDataGenerator(rescale=1./255)

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1
    )
    test_datagen = ImageDataGenerator(rescale=1./255)
    # target size의 HEIGHT, WIDTH는 위에서 정의해놓음
    # train_dir와 test_dir, validation_dir도 위에서 정의해놓음
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size = (IMG_SIZE[0], IMG_SIZE[0]),
        batch_size = 5,
        class_mode='categorical'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size = (IMG_SIZE[0],IMG_SIZE[0]),
        batch_size = 5,
        class_mode='categorical'
    )

    validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size = (IMG_SIZE[0],IMG_SIZE[0]),
        batch_size = 5,
        class_mode='categorical'
    )
    return train_generator, test_generator, validation_generator
