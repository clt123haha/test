import time

from flask import request

from data_sheet import session, ShortMessage
from utils.tool import short_message
from ..user import bp

@bp.route('/mobile_text')
def test():
    phone = request.json.get("phone")
    if phone is None:
        return {'code':201,'message':'请输入手机号码'}
    try:
         indonesia = short_message(phone)
    except Exception as e:
        print(e)
        return {'code':202,'meaasge':'发送失败，请稍后再试'}
    try:
        result = session.query(ShortMessage).filter(ShortMessage.phonenumber == phone).first()
        if result is None:
            newMessage = ShortMessage(phonenumber=phone,meaasge=indonesia,time=str(time.time()))
            session.add(newMessage)
            session.commit()
        else:
            result.meaasge = indonesia
            result.time = str(time.time())
            session.add(result)
            session.commit()
    except Exception as e:
        session.rollback()
        return {'code':203,'message':'验证码无效'}
    return  {'code':200,'message':'success'}