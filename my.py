from flask import Flask
from flask import request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from utils.log import log_testing

from api import user_bp,trade_bp,chat_bp,admin_bp,cheak_bp
#,pay_bp
from utils.tool import append
from data_sheet import get_sheet



app = Flask(__name__)
CORS(app, supports_credentials=True)

#有一个requests的删掉了
app.register_blueprint(user_bp)
app.register_blueprint(trade_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(cheak_bp)
#app.register_blueprint(pay_bp)
log_testing()
socketio = SocketIO(app)
@socketio.on('connect')
def test_connect(data):
    sid = data["socketid"]
    id = data["userid"]
    user = session.query(User).filter(User.id == id).first()
    user.sid = sid
    session.add(user)
    session.commit()
    emit('connect response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('getmessage')
def getmessage(data):
    id1 = request.json.get("userid")
    id2 = request.json.get("talkto")
    message = data["message"]
    sid = session.query(User).filter(User.id == id1).first().sid
    emit("getmeaasge", message, room=sid)
    append(id2, id1, message)
    append(id1, id1, message)


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    get_sheet()
    socketio.run(app, host='0.0.0.0', debug=True)