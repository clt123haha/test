import json

from fastapi import requests
from flask import request

from data_sheet import session, User
from utils import login_required
from ..user import bp

@bp.route("/IdentityAuthenticate",methods=['POST'])
@login_required
def authenticate():
    user_id = request.json.get("user_id")
    identity_card = request.json.get("identity_card")
    name = request.json.get("name")
    host = 'https://idenauthen.market.alicloudapi.com/idenAuthentication'
    AppCode = "93e6a698a46b48b984fa4bbbf4a2a2ea"  # AppCode只有购买后才能获得
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Authorization": 'APPCODE ' + AppCode}
    data = {"idNo": identity_card, "name":name}
    res = requests.post(host, data=data, headers=headers)
    if res.status_code == 200:
        result = json.loads(res.text)
        respMessage = result.get("respMessage")
        if respMessage != "身份证信息匹配":
            return {"code":205,"message":"身份信息错误"}
        birthday = result.get("birthday")
        user= session.query(User).filter(User.id == user_id).first()
        user.birthday = birthday
        session.add(user)
        session.commit()
        return {"code":200,"message":"认证成功"}
    return {"code":204,"message":"访问服务器失败，请稍后再试"}