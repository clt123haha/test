from flask import request
from flask_socketio import emit

from data_sheet import User
from data_sheet import session
from utils import login_required
from utils.tool import append
from ..chat import bp


@bp.route('/sendmessage',methods=["POST"])
@login_required
def sendmessage():
    try:
        id1 = request.json.get("uid")
        id2 = request.json.get("talkto")
        message = request.json.get("message")
        sid = session.query(User).filter(User.id == id2).first().sid
        emit("sendmeaasge",message,room = sid)
        append(id2,id1,message)
        append(id1, id1, message)
        return {"code":200,"message":"success"}
    except Exception as e:
        print(e)
        return {"code":405,"message":"fail"}