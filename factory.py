from flask import Flask
from flask_cors import CORS
from api import user_bp,trade_bp,chat_bp,admin_bp,cheak_bp
from utils import log_testing

def creat_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='LIUBINGZHEISBEST'
    #忽略的检查的url
    NOT_CHECK_URL=['/user/login','/user/reqister']
    CORS(app, supports_credentials=True)

    #有一个requests的删掉了
    app.register_blueprint(user_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cheak_bp)
    #app.register_blueprint(pay_bp)
    log_testing()
    return app
