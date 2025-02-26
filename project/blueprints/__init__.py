from flask import Flask, blueprints
from flask_mail import Mail
# 🔹 API 파일에서 Blueprint 가져오기
from .test import test_bp

mail = Mail()

# 🔹 Blueprint 리스트를 만들어서 한 번에 등록할 수 있도록 설정
blueprints = [test_bp]

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234'  # 반드시 고유한 비밀 키 사용

    from .member import member_bp
    app.register_blueprint(member_bp, url_prefix='/member')

    for bp in blueprints:
        app.register_blueprint(bp)

    return app