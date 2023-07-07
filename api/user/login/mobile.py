from fastapi import requests
from flask import request

from api.user import bp
from data_sheet import session, User
from utils.tool import check_Indonesia, check_message
from utils.token import create_token


#验证手机验证码的登录接口
@bp.route('/login/moblie',methods=['POST'])
def moblie_login():
    indonesia = requests.get("Indonesia")
    message = request.json.get("message")
    phone = request.json.get("phone")
    ischeak = check_Indonesia(indonesia)
    ischeak2 = check_message(phone,message)
    result = session.query(User).filter(User.phone == phone).first()
    token = create_token(result.id)
    if result is None:
        return {'code': 302, 'message': '账号不存在'}
    if ischeak == True and ischeak2 == True:
        return {'code':200,'message':'success','data':{'id':result.id,"token":token}}
    if ischeak == False:
        return {'code': 304, 'message': '验证码错误'}
    if ischeak2 == False:
        return {'code': 305, 'message': '手机验证码错误'}