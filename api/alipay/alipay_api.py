import time
import alipay_config as alipay_config_class
from flask import Blueprint
import alipay_submit_class
import alipay_notify_class

bp = Blueprint("alipay",__name__,static_folder='/alipay')

@bp.route('/alipay')
def alipay_pay(data = {}):
    config_ = alipay_config_class.alipay_config()

    time_ = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    out_trade_no = data['WIDout_trade_no'] if data['WIDout_trade_no'] else ''
    if out_trade_no == '':
        return ''

    #支付类型
    payment_type = "1";
    notify_url =  data['notify_url']

    #页面跳转同步通知页面路径
    return_url = data['return_url']

    #商户订单号
    out_trade_no = data['WIDout_trade_no']

    #订单名称
    subject = data['WIDsubject'] if data.has_key('WIDsubject') else "duobao_pay"

    #付款金额
    total_fee = data['WIDtotal_fee']
    #商品展示地址
    show_url = data['WIDshow_url'] if data.has_key('WIDshow_url') else data['return_url']

    #超时的时间
    overtime = data['WIDit_b_pay'] if data.has_key('WIDit_b_pay') else 86400

    parameter = {
            "service"  : "alipay.wap.create.direct.pay.by.user",
            "partner": config_['partner'],
            "seller_id": config_['seller_id'],
            "payment_type": payment_type,
            "notify_url": notify_url,
            "return_url": return_url,
            "out_trade_no": out_trade_no,
            "subject": subject,
            "total_fee": total_fee,
            "show_url": show_url
        }

    #建立请求
    alipaySubmit = alipay_submit_class.AlipaySubmit(config_)

    html_text = alipaySubmit.buildRequestUrl(parameter)   
    return html_text

# 支付宝异步
@bp.route('/alipay_result')
def notify_url(request_data) :
    config_ = alipay_config_class.alipay_config()
    alipayNotify = alipay_notify_class.AlipayNotify(config_)
    verify_result = alipayNotify.verifyNotify(request_data)
    if verify_result :
        return {"code":200,"message":"成功了"}
    else :
        return {"code":404,"message":"出错了"}

#返回信息
@bp.route('/alipay_message')
def get_conf():
    config_ = alipay_config_class.alipay_config()
    list= {
            'seller_id' : config_['seller_id'],
            'key' :config_['key']  ,
            'partner':config_['partner'] ,
            'account_name': config_['account_name']
        }
    return {"code":200,"data":list,"message":"成功支付"}