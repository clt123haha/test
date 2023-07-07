from flask import request

from utils import login_required
from ..cheak import bp

@bp.route('/checking1')
@login_required
def check1():
    checking1=request.json.get("checking1")
    try:
        if checking1==1:
            return {"code": 200, "message": "审核通过，账号已上架"}
        if checking1==0 :
            return{"code":200,"message":"审核未通过，账号无法上架"}
        if checking1==None:
            return{"code":200,"message":"仍在审核中，请稍后"}
    except Exception as e:
        print(e)
        return{"code":404,"message":"出错了"}