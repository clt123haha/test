from flask import request
from ..cheak import bp

@bp.route('/checking2')
def check2():
    checking1=request.json.get("checking1")
    checking2 = request.json.get("checking2")
    try:
        if checking1==1 and checking2==1:
            return {"code": 200, "message": "审核通过，请支付"}
        if checking1==1 and checking2==0 :
            return{"code":200,"message":"审核未通过"}
        if checking2==None:
            return{"code":200,"message":"仍在审核中，请稍后"}
    except Exception as e:
        print(e)
        return{"code":404,"message":"出错了"}