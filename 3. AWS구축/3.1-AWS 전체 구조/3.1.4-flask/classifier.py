import os
from tensorflow.keras import models
from PIL import Image
import numpy as np

# dataset의 종류 리스트
model_color = models.load_model('./data/model/color.h5')
model_cloth = models.load_model('./data/model/clothes.h5')

def get_cloth(image):

    # 이미지 resize
    img = Image.open(image)
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
    img = Image.open(image)
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

if __name__ == '__main__':
    # module test code
    my_cloth = get_cloth('./test_data/test_baji.jpg')
    my_color = get_color('./test_data/test_baji.jpg')
    print(my_cloth)
    print(my_color)
