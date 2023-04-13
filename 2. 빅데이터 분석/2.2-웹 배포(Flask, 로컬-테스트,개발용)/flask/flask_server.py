import boto3, requests, csv
import json, os
from flask import Flask, render_template, request, session, escape, jsonify
from werkzeug.utils import secure_filename
import similar
import connect_db
# import transformer

s3 = boto3.client('s3')
API_URL = "https://2q57tqhq5m.execute-api.ap-northeast-2.amazonaws.com/predict"

# HTTP 서버 실행하기
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

color_list = ['베이지색', '검정색', '갈색', '회색', '초록색', '파란색', '빨간색', '하얀색']
cloth_list = ['긴팔티셔츠', '셔츠', '맨투맨_후드', '면바지', '반바지', '반팔', '블라우스', 
 '스커트', '원피스', '청바지', '카디건', '트레이닝복']

# web 렌더링
@app.route("/", methods=['GET'])
def index() :
  return render_template('index.html')

@app.route("/upload", methods=['GET','POST'])
def upload() :
  return render_template('upload.html')


# app 부분
#########################
# CNN 예측
#########################
@app.route('/cnn_process', methods=['GET','POST'])
def cnn_process():
  # file과 file 이름 가져오기
  f = request.files['file']
  print(f)
  filename = secure_filename(f.filename)
  img_local_url = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\','/')
  print(img_local_url)
  f.save(img_local_url) 
  
  # CNN으로 옷 종류, 색깔 판별
  # json은 numpy type 못받으므로 int로 형변환
  # cloth = int(classifier.get_cloth(f))
  # color = int(classifier.get_color(f))


  bucket_name = "thunder-model-bucket"
  image_uri = "predict_img/" + filename
  s3.upload_file(img_local_url, bucket_name, image_uri)

  URL = API_URL + "/clothcolor"
  data = {"bucket":bucket_name, "image_uri":image_uri}
  res = requests.post(URL, data=json.dumps(data))

  # print(res.json())

  result = res.json()
  print(result)

  cloth = result['cloth']
  color = result['color']

  print(color)
  print(cloth)


  # 옷 종류와 색깔 json으로 dump
  return json.dumps({
    "cloth": cloth,
    "color": color
  })

#########################
# Cosine 프로세스 부분
#########################
@app.route('/cosine_process', methods=['GET','POST'])
def cosine_process():
  # file 가져오기
  f2 = request.files['file']

  # Json으로 Post받은 카테고리 가져오고 int로 변환
  category = int(request.form.get("category"))

  # cosine 유사도로 비슷한 이미지의 가격정보 가져오기
  result = similar.get_similar(f2, category)
  # print(category)
  # print(result)

  # 최대, 최소, 평균 가격 json으로 dump
  return json.dumps({
    "mean": result[0],
    "img1": result[1][0],
    "img2": result[1][1],
    "img3": result[1][2],
    "sim1": result[2][0],
    "sim2": result[2][1],
    "sim3": result[2][2],
    "pri1": result[3][0],
    "pri2": result[3][1],
    "pri3": result[3][2]
  })

#########################
# rnn 문장 생성하는 부분 (폐기)
#########################
# @app.route('/rnn_process', methods=['GET','POST'])
# def rnn_process():

#   # Json으로 Post받은 카테고리 가져오고 int로 변환
#   data = request.get_json()
#   category = int(data['category'])

#   # category를 문자로 바꿈
#   category = cloth_list[category]
#   print(category)

#   # 카테고리를 시드로 문장 생성
#   URL = API_URL + "/rnn"
#   data = {"word":category}
#   res = requests.post(URL, data=json.dumps(data))

#   result = res.json()
#   print(result)

#   result = result["result_text"]

#   # 생성한 문장 json으로 dump
#   return json.dumps({
#   "text": result
#   })

################################
# transformer 문장 예측하는 부분
################################
@app.route('/transformer_process', methods=['GET','POST'])
def transformer_process():

  # Json으로 Post받은 카테고리 가져오고 int로 변환
  data = request.get_json()
  category = int(data['category'])
  color = int(data['color'])
  size = data['size']
  washing = data['washing']

  # category를 문자로 바꿈
  category = cloth_list[category]
  color = color_list[color]
  print(category)
  print(data)

  # 카테고리를 시드로 문장 생성
  URL = API_URL + "/transformer"
  data = {
    "category" : category,
    "color" : color,
    "size" : size,
    "washing" : washing,
    'content_type': "application/json"
  }
  res = requests.post(URL, data=json.dumps(data))

  result = res.json()
  print(result)

  result = result["result_text"]
  # request_text = category + "," + color + "," + size + "," + washing
  # result = transformer.predict(request_text)

  # 생성한 문장 json으로 dump
  return json.dumps({
  "text": result
  })

#########################
# 파일 및 DB 정보 업로드
#########################
@app.route('/upload_process', methods=['GET','POST'])
def upload_process():

  # form에서 이미지 받아오기
  f3 = request.files['file']

  # 이미지 이름 가져오기
  filename = secure_filename(f3.filename)

  # form data 받아오기
  q = request.form
  print(q)
  
  # db에 업로드하기
  connect_db.query(connect_db.upload(q['title'],int(q['price']),q['contents'],q['deliver'],
                  q['status'],color_list[int(q['color'])],q['washing'],q['size'],int(q['category'])))

  query = connect_db.query_select(connect_db.select_img_id())

  img_id = int(query['pd_id'])

  # print(filename)
  filename = str(img_id) + '.jpg'
  # print(filename)

  # 업로드 ( .save(경로) )
  img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\','/')
  f3.save(img_url) 
  
  bucket = "thunder-model-bucket"

  f = open('../access.csv','r')
  rdr = csv.reader(f)
  access=[]
  for line in rdr:
      access.append(line)

  # 지울 코드(local)
  s3 = boto3.client('s3', aws_access_key_id=access[0][0], aws_secret_access_key=access[0][1])
  # 살릴 코드
  # s3 = boto3.client('s3')

  s3.upload_file(img_url, bucket, "img_product/"+filename)

  connect_db.query(connect_db.upload_image(img_id, img_id, img_url, 'jpg'))
              
  return render_template('upload_complete.html')


# 서버 구동
if __name__ == '__main__':
  app.run(host="0.0.0.0", port="80")