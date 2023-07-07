from flask import request
from sqlalchemy.sql.elements import or_

from api.user import bp
from data_sheet import session, User
from utils.tool import check_Indonesia
from utils.token import create_token


@bp.route('/login/password',methods=['POST'])
def check_password():
    print(request.json)
    account = request.json.get("account")
    password = request.json.get("password")
    indonesia = request.json.get("Indonesia")
    indonesia = str(indonesia).lower()
    if account is None or password is None:
        return {"code":306,"message":"信息不全"}
    '''ischeak = check_Indonesia(indonesia)'''
    result = session.query(User).filter(or_(User.phone==account, User.email==account)).first()
    toekn = create_token(result.id)
    #if ischeak == False:
        #return {'code': 304, 'message': '验证码错误'}
    if result == None:
        return {'code': 302, 'message': '账号不存在'}
    if result.password != password:
        return {'code': 303, 'message': '密码错误'}
    return {'code':200,'message':'success','data':{'id':result.id,"token":toekn}}