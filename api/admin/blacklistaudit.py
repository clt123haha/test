from flask_socketio import emit
from ..admin import bp
from flask import request

from data_sheet import session, Audit, Blacklist


@bp.route('/blacklistaudit',methods=['POST'])
def blacklistauditing():
    opinion = request.json.get("opinion")
    aid = request.json.get("aid")
    if type is None or opinion is None or aid is None:
        return {"code": 201, "message": "信息不全"}
    audit = session.query(Audit).filter(Audit.id == aid).first()
    sid = 1#session.query(User).filter(User.id == audit.uid).first().sid
    if audit is None:
        return {"code": 201, "message": "没有这条审核信息"}
    if audit.type != "block":
        return {"code": 201, "message": "审核类型提交有误"}
    try:
        if opinion == True:
            audit.ifpass = True
            newBlackList = Blacklist(uid = audit.message)
            session.add(newBlackList)
            session.add(audit)
            session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return {"code": 307, "message": "信息存储失败"}
    try:
        if opinion == True:
            emit("sendmeaasge", "成功拉黑用户 " + audit.message, room=sid,namespace='/chat')
        else:
            emit("sendmeaasge", "审核未通过，不可拉黑用户 " + audit.message, room=sid,namespace='/chat')
    except Exception as e:
        session.rollback()
        print(e)
        return {"code": 307, "message": "消息发送失败"}
    return {"code": 200, "message": "success"}