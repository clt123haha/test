import base64
import itertools

from flask import session

from utils import login_required
from ..trade import bp

from flask import request
import os
from data_sheet import session, Transaction


@bp.route("/gettransaction",methods=["POST"])
@login_required
def gettransaction():
    id= request.json.get("tid")
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
        photolist = []
        file_path = r'E:\trade\account' + '\\' + str(id) + '\\' + str(id) + ".txt"
        if not os.path.exists(file_path):  # 检测目录是否存在，不在则创建
            return {'code': 302, 'message': '交易信息不存在'}
        f = open(file_path, 'r')
        for line in f:
            message += line
        for i in itertools.count(start=1):
            file_path = r'E:\trade\account' + '\\' + str(i) + '\\' + str(id) + ".png"
            if not os.path.exists(file_path):  # 检测目录是否存在，不在则创建
                break
            with open(file_path, 'rb') as f:
                photolist.append(str(base64.b64encode(f.read())))
        data = {"tid":result.id,"price": price, "channel": channel, "login_method": login_method, "message": message, "system": system,
            "addiction": addiction, "seller": result.seller,"photo":photolist}
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息获取失败，请稍后再试"}
    return {"code":200,"message":"success","data":data}
