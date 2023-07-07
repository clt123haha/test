#import alipay_core_function
#import alipay_md5_function
import utils
import time
import urllib
from io import StringIO
import pycurl
import _md5

"""
 * 签名字符串
 * @param $prestr 需要签名的字符串
 * @param $key 私钥
 * return 签名结果
 """
def md5Sign(prestr, key) :
    prestr = "%s%s" % (prestr, key)
    m1 = _md5.new()
    m1.update(prestr)
    return m1.hexdigest()

"""
 * 验证签名
 * @param $prestr 需要签名的字符串
 * @param $sign 签名结果
 * @param $key 私钥
 * return 签名结果
 """
def md5Verify( prestr, sign, key) :
    prestr = "%s%s" % (prestr, key)
    m1 = _md5.new()
    m1.update(prestr)
    mysgin = m1.hexdigest()
    if mysgin == sign :
        return True
    else :
        return False

def md5my_token(prestr, key):
    prestr = "%s%s" % (prestr, key)
    m1 = _md5.new()
    m1.update(prestr)
    return m1.hexdigest()

def my_urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

#转义字符
def createLinkstring(para, keys=[]) :
    arg = ""
    if len(keys)>0:
        for k in keys:
            arg += "%s=%s&" %(str(k), str(para[k]))
    else :
        for i in para :
            arg += "%s=%s&" %(str(i), str(para[i]))
    return arg[:-1]

def createLinkstringUrlencode(para,keys = []) :
    arg = ""
    if len(keys)>0:
        for k in keys:
             arg += "%s=%s&" %(k, my_urlencode(para[k]))
    else :
        for i in para :
            arg += "%s=%s&" %(i, my_urlencode(para[i]))
    return arg[:-1]

def paraFilter(para) :
    para_filter = {}
    for key in para :
        if key=="sign" or key == "sign_type" or para[key] == "" or para[key] == "key":
            continue
        para_filter[key] = para[key]
    return para_filter

def argSort(para) :
    keys = para.keys()
    keys.sort()
    return keys

def logResult(word='') :
    file_object = open('log.txt', 'a')
    time_ = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    file_object.write(" 执行日期:\n %s \n" %(time_, word))
    file_object.close( )

def getHttpResponsePOST(url, cacert_url, para, input_charset = '') :
    if input_charset.lstrip() != '':
        url = "%s_input_charset=%s" %(url,  input_charset )
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, f.write)
    curl.setopt(pycurl.SSL_VERIFYPEER, 1)   #SSL证书认证
    curl.setopt(pycurl.SSL_VERIFYHOST, 2)  #严格认证
    curl.setopt(pycurl.CAINFO, cacert_url) #证书地址
    curl.setopt(curl.HEADER, 0)  # CURLOPT_HEADER
    curl.setopt(curl.POSTFIELDS, urllib.urlencode(para))  # post传输数据
    curl.perform()
    responseText = ''
    if curl.getinfo(pycurl.RESPONSE_CODE) == 200:
        responseText = f.getvalue()
    curl.close()
    f.close()
    return responseText

"""
 * 远程获取数据，GET模式 (这里就用request算了)
 * 注意：
 * 1.使用Crul需要修改服务器中php.ini文件的设置，找到php_curl.dll去掉前面的";"就行了
 * 2.文件夹中cacert.pem是SSL证书请保证其路径有效，目前默认路径是：getcwd().'\\cacert.pem'
 * @param $url 指定URL完整路径地址
 * @param $cacert_url 指定当前工作目录绝对路径
 * return 远程输出的数据
 """
def  getHttpResponseGET(url, cacert_url ) :
    import requests
    r = requests.get(url)
    responseText = r.text
    '''
    curl = pycurl.Curl()
    f = StringIO.StringIO()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEFUNCTION, f.write)
    curl.setopt(pycurl.SSL_VERIFYPEER, 1)   #SSL证书认证
    curl.setopt(pycurl.SSL_VERIFYHOST, 2)  #严格认证
    curl.setopt(pycurl.CAINFO, cacert_url) #证书地址
    # curl.setopt(pycurl.SSLCERTTYPE, "PEM")  
    # curl.setopt(pycurl.SSLCERT, '/home/youmi/Desktop/sys/wap_alipay/alipay_batch_trans/cacert.pem')
    curl.setopt(curl.HEADER, 0)  # CURLOPT_HEADER
    # curl.setopt(pycurl.CURLOPT_HTTPPOST, 1)  # post传输数据
    # curl.setopt(curl.POSTFIELDS, urllib.urlencode(para))  # post传输数据
    # curl.setopt(pycurl.HEADERFUNCTION, headerCookie)
    # curl.setopt(pycurl.COOKIE,Cookie)
    curl.perform()
    responseText = f.getvalue()
    curl.close()
    f.close()
    '''
    return responseText

""""
 * 实现多种字符编码方式
 * @param $input 需要编码的字符串
 * @param $_output_charset 输出的编码格式
 * @param $_input_charset 输入的编码格式
 * return 编码后的字符串
 """
def charsetEncode( input, _output_charset , _input_charset):
    if not _output_charset :
        _output_charset = _input_charset

    if (_input_charset == _output_charset) or not input :
        output = input
    else :
        output = input.encode(_output_charset)
    return output

class AlipayNotify :
    
    # HTTPS形式消息验证地址
    https_verify_url = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'
    
    #HTTP形式消息验证地址
    http_verify_url = 'http://notify.alipay.com/trade/notify_query.do?'
    alipay_config = ''

    def __init__(self, alipay_config) :
        self.alipay_config = alipay_config
    
    def AlipayNotify(self, alipay_config) :
        self.__init__(alipay_config)

    def verifyNotify (self, request_data) :
        print ("=request_data:%s=" %request_data)
        if len(request_data) ==0 :     #判断POST来的数组是否为空
            print('request_data error!')
            return False
        else :
            if request_data.has_key('out_trade_no')==False  or request_data['out_trade_no']=='':
                print ('out_trade_no error!')
                return False

            if request_data.has_key('trade_no')==False  or request_data['trade_no']=='':
                print ('trade_no error!')
                return False

            if request_data.has_key('pay_sign')==False or request_data['pay_sign']=='' :
                print ('==%s: pay_sign error!==' % (request_data['trade_no'] ))
                return False

            isSign = False
            # isSign = self.getSignVeryfy(request_data, request_data["sign"])
            isSign = self.getSignVeryfy2(request_data['out_trade_no'], request_data["pay_sign"])

            #获取支付宝远程服务器ATN结果（验证是否是支付宝发来的消息）
            responseTxt = 'false'
            if request_data.has_key('notify_id') == True :
                responseTxt = self.getResponse( request_data["notify_id"])
            
            log_text = "notify_url_log:out_trade_no:%s, responseTxt=%s ,isSign=%s, pay_sign=%s,  key=%s," % (request_data['out_trade_no'], responseTxt, isSign, request_data["pay_sign"], self.alipay_config['key'])
            print ("=%s=" %log_text)
            '''
            # logResult($log_text);
            # utils.loggers.use('pay_alipay', send_log_file_).info("TransnotifyurlHandler_verifyNotify,%s" % (log_text))
            file_object = open('verifyNotify_logs.log', 'a')
            time_ = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            file_object.write("[%s],%s\n" %(time_, log_text))
            file_object.close( )
            '''
            try:
                utils.loggers.use('pay_alipay', '/home/deploy/log/duobao/pay_alipay.log').info("%s"% (log_text))
            except:
                pass

            if responseTxt .strip() == 'true' and isSign==True:
                return True
            else :
                return False

    def verifyReturn(self, request_data) :
        if len(request_data)==0 :      #判断POST来的数组是否为空
            return False
        else :
            #生成签名结果
            isSign = self.getSignVeryfy(request_data, request_data["sign"]);
            
            #获取支付宝远程服务器ATN结果（验证是否是支付宝发来的消息）
            responseTxt = 'false'
            if request_data.has_key('notify_id') == True :
                responseTxt = self.getResponse(request_data["notify_id"])

            if responseTxt == 'true' and isSign !='' :
                return True
            else :
                return False

    def getSignVeryfy(self, para_temp,  sign) :

        para_filter = paraFilter(para_temp)

        keys = argSort(para_filter)

        prestr = createLinkstring(para_filter, keys)
        
        isSgin = False
        if self.alipay_config['sign_type'].upper() == 'MD5':
            isSgin = md5Verify(prestr, sign, self.alipay_config['key'])

        elif self.alipay_config['sign_type'].upper() == 'RSA':
            pass
        else :
            isSgin = False
        return isSgin

    # 只验证 out_trade_no 加密
    def getSignVeryfy2(self, out_trade_no, sign):
        return md5Verify(out_trade_no, sign, self.alipay_config['key'] )

    def getResponse(self, notify_id) :
        transport = self.alipay_config['transport'].strip().lower()
        partner = self.alipay_config['partner'].strip()
        veryfy_url = ''
        
        if transport == 'https' :
            veryfy_url = self.https_verify_url
        else :
            veryfy_url = self.http_verify_url
        
        veryfy_url = "%spartner=%s&notify_id=%s" %(veryfy_url, partner, notify_id)
        responseTxt = getHttpResponseGET(veryfy_url, self.alipay_config['cacert'])
        
        return responseTxt