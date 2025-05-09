import pymysql

# 📌 MySQL 연결 함수 (모든 API에서 재사용 가능)
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='vndgh3538',
        database='flask_root1234',
        charset='utf8mb4',
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )

# 📌 파일 업로드 허용 확장자 검사
# def allowed_file(filename):
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
