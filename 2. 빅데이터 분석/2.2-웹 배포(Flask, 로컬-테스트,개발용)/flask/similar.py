import os, boto3, csv
import pandas as pd
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import platform

# dataset의 종류 리스트
cloth_list = ['긴팔티셔츠', '셔츠', '맨투맨_후드', '면바지', '반바지', '반팔', '블라우스', 
              '스커트', '원피스', '청바지', '카디건', '트레이닝복']

def search(dirname):
    search_list = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        search_list.append(full_filename)
    return search_list

def get_similar(image, category):
    # directory 설정
    if platform.system()=='Windows':
        root_dir = '.\\data'
    else:
        root_dir = './data'

    img = Image.open(image)
    img = img.convert("RGB")
    img = img.resize((64,64))
    data = np.asarray(img)

    img_np = np.array(data)
    img_np = img_np.astype("float") / 255
    img_np = img_np.reshape(1, -1)

    result = []
    # category로 읽어와야 함

    meta_dir = search(os.path.join(root_dir, 'meta'))
    npy_dir = search(os.path.join(root_dir, 'npy'))
    pickle_dir = search(os.path.join(root_dir, 'pickle'))
    # img_dir = search(os.path.join('.\\static', 'img'))

    img_dir = []

    # npy, list 읽어오기
    img_list = np.load(npy_dir[category])

    with open(pickle_dir[category], 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for i,line in enumerate(rdr):
            img_path_list = line
    # meta-data 불러오기
    meta = pd.read_csv(meta_dir[category], encoding='utf-8')

    # cosine 비교
    for i in range(len(img_list)):
        similarity_simple_pair = cosine_similarity(img_np, img_list[i])
        result.append(similarity_simple_pair)

    # list_df의 img_id 데이터 경로에서 숫자값만 추출
    img_id_list = []
    img_id_ub_list = []

    for i in range(len(img_path_list)):
        k = os.path.basename(img_path_list[i])
        k = os.path.splitext(k)
        img_id_list.append(int(k[0].split('_')[0]))
        img_id_ub_list.append(int(k[0].split('_')[1]))

    # 데이터 프레임 생성
    data = pd.DataFrame({'img_id':img_id_list, 'img_id_ub':img_id_ub_list, 'num':result})
    data = data.sort_values(by='num', ascending=False)
    data = data.reset_index(drop=True)
    data = data.drop_duplicates('img_id', keep = 'first')
    data.reset_index(drop=True, inplace=True)


    test2 = pd.merge(data, meta, on='img_id')
    test3 = test2[['img_id', 'img_id_ub', 'num', 'price']][:10]

    # 데이터 정제
    test3['price'] = test3['price'].str.replace('원',' ')
    test3['price'] = test3['price'].replace({',': ''}, regex=True)
    test3['price'] = pd.to_numeric(test3['price'])

    print(test3.head(5))

    # 유사도 높은 상위 10개 상품의 가격을 매기기
    p_mean = int(test3['price'].mean())
    p_num = []
    p_price = []
    p_img_id = []
    bucket_img_url = []

    bucket_url = "cosinedata/"
    bucket_dir_list = ["01_ginpal/", "02_shirt/", "03_mantoman/", "04_ginbaji/", "05_banbaji/", "06_banpal/", "07_blouse/", "08_skirt/", "09_onepiece/", "10_bluejean/", "11_cardigan/", "12_training/"]

    for i in range(3):
        num = test3['num'][i][0][0]
        num = str(round(num * 100, 2))+"%"
        img_id = str(test3['img_id'][i]) + "_" + str(test3['img_id_ub'][i]) + ".jpg"
        bucket_img_id = bucket_url + bucket_dir_list[category] + img_id
        price = test3['price'][i]
        price = "{:,}".format(price)

        print(img_id)
        print(bucket_img_id)
        print(num)
        print(price)

        p_img_id.append(img_id)
        p_num.append(num)
        p_price.append(price)
        bucket_img_url.append(bucket_img_id)

    result = [p_mean, p_img_id, p_num, p_price]

    bucket = "thunder-model-bucket"

    # f = open('../access.csv','r')
    # rdr = csv.reader(f)
    # access=[]
    # for line in rdr:
    #     access.append(line)

    # 지울 코드(local)
    # s3 = boto3.client('s3', aws_access_key_id=access[0][0], aws_secret_access_key=access[0][1])
    # 살릴 코드
    s3 = boto3.client('s3')

    for i in range(3):
        p_img_id[i] = "./static/cosine_img/"+p_img_id[i]
        s3.download_file(bucket, bucket_img_url[i], p_img_id[i])

    return result

if __name__ == '__main__':
    # module test code
    my_cloth = get_similar('./test_data/test_baji.jpg', 4)
    print('평균가 : {}원'.format(my_cloth[0]))
    print(my_cloth)
    # print(my_cloth[1][0])
