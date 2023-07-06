import os
 
def alipay_config():
    alipay_config = {}

    alipay_config['key']           = ''

    alipay_config['seller_id']   = ''

    alipay_config['account_name'] = u""

    alipay_config['sign_type']    = 'MD5'.upper()

    alipay_config['input_charset'] = 'utf-8'.lower()

    alipay_config['cacert']    = os.getcwd()+'\\cacert.pem'

    alipay_config['transport']    = 'https'

    return alipay_config