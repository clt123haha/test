from flask import request
from flask_socketio import emit

from data_sheet import User
from data_sheet import session
from utils.tool import append
from ..chat import bp


@bp.route('/sendmessage')
def sendmessage():
    id1 = request.json.get("userid")
    id2 = request.json.get("talkto")
    message = request.json.get("message")
    sid = session.query(User).filter(User.id == id2).first().sid
    emit("sendmeaasge",message,room = sid)
    append(id2,id1,message)
    append(id1, id1, message)