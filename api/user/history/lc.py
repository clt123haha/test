from flask import request, jsonify
from sqlalchemy import and_

from data_sheet import session, User_History, History
from api.user import bp
from utils import login_required


@bp.route('/history/lc', methods=['PUT'])
@login_required
def lc():
    message = request.get_json()
    hid = message.get('hid')
    fav = message.get('fav')
    id=message.get('id')
    f = session.query(User_History).filter(and_(User_History.id==id,User_History.history==hid)).first()
    history = session.query(History).filter(History.id==hid).first()
    if not history:
        return jsonify(code=404,message='没有找到该记录')
    else:
        f.fav=fav
        session.commit()
        dict={
            'gamename':history.gamename,
            'rid':history.rid
        }
        return jsonify(code=200,message='success',data=dict)