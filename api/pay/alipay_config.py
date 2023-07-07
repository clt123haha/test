import os
 
def alipay_config():
    #↓↓↓↓↓↓↓↓↓↓请在这里配置您的基本信息↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    alipay_config = {}

    #安全检验码，以数字和字母组成的32位字符
    alipay_config['key']           = ''

    #↑↑↑↑↑↑↑↑↑↑请在这里配置您的基本信息↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    alipay_config['seller_id']   = ''

    alipay_config['account_name'] = u""

    alipay_config['sign_type']    = 'MD5'.upper()

    alipay_config['input_charset'] = 'utf-8'.lower()

    alipay_config['cacert']    = os.getcwd()+'\\cacert.pem'

    alipay_config['transport']    = 'https'

    return alipay_config