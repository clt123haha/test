from flask import request

from utils import login_required
from ..trade import bp
from data_sheet import session,Audit

@bp.route("buy",methods=["POST"])
@login_required
def buy():
    message = str(request.json.get("message"))
    aid = request.json.get("aid")
    if message == "成功支付":
        audit = session.query(Audit).filter(Audit.id == aid).first()
        audit.message = "已支付"
        session.add(audit)
        session.commit()
    return {"code":200,"message":"success"}

