import pymysql

# database에 연결하는 함수
# def connect_db(database):
#     # DB 호스트 정보에 맞게 입력해주세요
#     db = None
#     db = pymysql.connect(
#         host='beyonddb.codfzx35ubid.ap-northeast-2.rds.amazonaws.com',
#         user='root',
#         passwd='password123',
#         db=database,
#         charset='utf8',
#         port=3306
#     )
#     return db

def connect_db(database):
    # DB 호스트 정보에 맞게 입력해주세요
    db = None
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='password123',
        db=database,
        charset='utf8',
        port=3306
    )
    return db

# database에 쿼리를 날리는 함수
def query(sql_query):
    db = None
    try:
        db = connect_db('beyond')
        
        with db.cursor() as cursor:
            sql = sql_query
            cursor.execute(sql)
        db.commit() # 커밋

    except Exception as e:
        print(e)

    finally:
        if db is not None:
            db.close()

def query_select(sql_query):
    db = None
    result = ''
    try:
        db = connect_db('beyond')
        
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = sql_query
            cursor.execute(sql)
            result = cursor.fetchone()
    except Exception as e:
        print(e)

    finally:
        if db is not None:
            db.close()    
    return result

# database 회원가입 sql문을 만드는 함수
def register(email, passwd, name, town, phone, gender):
    sql = '''
            INSERT INTO user(user_email, user_passwd, user_name, user_town, user_phone, user_gender) values("%s", "%s", "%s", "%s", "%s", "%s")
            ''' % (email, passwd, name, town, phone, gender)
    return sql

# database 상품 업로드 sql문을 만드는 함수
def upload(title,price,contents,deliver,status,color,washing,size,category_id):
    sql = '''
            INSERT INTO product(pd_title, pd_price, pd_contents, pd_deliver, pd_status, pd_color, pd_washing, pd_size, category_id) values("%s", %d, "%s", "%s", "%s", "%s", "%s", "%s", %d)
            ''' % (title, price, contents, deliver, status, color, washing, size, category_id)
    return sql

# database 상품 업로드 sql문을 만드는 함수
def upload_image(img_id, pd_id, img_url, img_type):
    sql = '''
            INSERT INTO image values(%d, %d, "%s", "%s")
            ''' % (img_id, pd_id, img_url, img_type)
    return sql

def select_img_id():
    sql = '''
            SELECT pd_id FROM product ORDER BY pd_date DESC LIMIT 1;
            '''
    return sql

def select(title,price,contents,deliver,status,color,washing,size,category_id):
    sql = '''
            SELECT * from product(pd_title, pd_price, pd_contents, pd_deliver, pd_status, pd_color, pd_washing, pd_size, category_id) values("%s", %d, "%s", "%s", "%s", "%s", "%s", "%s", %d)
            ''' % (title, price, contents, deliver, status, color, washing, size, category_id)
    return sql

if __name__ == '__main__':
    # module test code
    # register('zebok@naver.com', 'password123', '이준호', '서울시 종로구', '010-5125-8988', 'M')
    # query(register('lisemara765@gmail.com', 'password', '이여름', '서울시 은평구', '010-1234-5678', 'F'))
    # result_query = query_select(select_img_id())
    # print (result_query)
    img_url = '10'
    
    query(upload("후드티 팝니다2",27000,"가나다라마바사","직거래","중고","파란색","드라이클리닝","M",3))
    query(upload_image(1, 1, "hello.jpg", "jpg"))
    