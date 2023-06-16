from flask import session
from ..trade import bp

from flask import request
import os
from data_sheet import session, Transaction


@bp.route("/get_transaction")
def get_transaction():
    id= request.json.get("id")
    result = session.query(Transaction).filter(Transaction.id == id).first()
    if result is None:
        return {"code":302,"message":"这条商品信息不存在"}
    price = result.price
    channel = result.channel
    login_method = result.login_method
    system = result.system
    addiction = result.addiction
    approved = result.approved
    message = ""
    if approved == 0:
        {"code": 402, "message": "该账号为通过审核，不可进行交易"}
    try:
        file_path = r'E:\trade\account' + '\\' + str(id) + ".txt"
        if not os.path.exists(file_path):  # 检测目录是否存在，不在则创建
            return {'code': 302, 'message': '简历不存在'}
        f = open(file_path, 'r')
        for line in f:
            message += line
        data = {"price": price, "channel": channel, "login_method": login_method, "message": message, "system": system,
            "addiction": addiction, "seller": result.seller}
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息获取失败，请稍后再试"}
    return {"code":200,"message":"success","data":data}
