from data_sheet import session, Audit, User
from flask import request
from ..user import bp


@bp.route('/newblock',methods=['POST'])
def newblock():
    uid = request.json.get("uid")
    blocked_uid = request.json.get("blocked_uid")
    if uid is None or blocked_uid is None:
        return {"code": 201, "message": "信息不全"}
    try:
        newAudit = Audit(uid=uid, ifpass=False, message=str(blocked_uid), type="block")
        session.add(newAudit)
        session.commit()
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息存储失败"}
    return {"code": 200, "message": "success"}
