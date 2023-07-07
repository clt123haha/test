from flask import request
from data_sheet import session,Collection
from utils import login_required
from ..user import bp

@bp.route("/collcte",methods=['POST'])
@login_required
def collcte():
    uid = request.json.get("uid")
    tid = request.json.get("tid")
    try:
        newCollection = Collection(uid=uid,tid=tid)
        session.add(newCollection)
        session.commit()
        return {"code":200,"message":"success"}
    except Exception:
        print(Exception)
        return {"code":308,"message":"数据储存出错"}