#import alipay_core_function
#import alipay_md5_function
import urllib
from hashlib import md5
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
    m1 = md5.new()
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
    m1 = md5.new()
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
    keys = sorted(para.keys())
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

class AlipaySubmit:
    alipay_config = ""
    alipay_gateway_new = 'https://mapi.alipay.com/gateway.do?'

    def __init__(self, alipay_config) :
        self.alipay_config = alipay_config

    def AlipaySubmit(self, alipay_config) :
        self.__init__(alipay_config)

    def buildRequestMysign(self, para_sort) :
        keys = argSort(para_sort)
        prestr = createLinkstring(para_sort, keys)
        print ("==%s=%s==" %(para_sort, prestr))
        if self.alipay_config['sign_type'].upper()  == 'MD5':
            mysign = md5Sign(prestr, self.alipay_config['key'])
        else :
            mysign = ""
        return mysign

    def buildRequestPara(self, para_temp) :
        #除去待签名参数数组中的空值和签名参数
        para_sort = paraFilter(para_temp)
        mysign = self.buildRequestMysign(para_sort)

        para_sort['sign'] = mysign
        para_sort['sign_type'] = self.alipay_config['sign_type'].upper()
        
        return para_sort

    def buildRequestForm(self, para_temp, method, button_name) :

        para = self.buildRequestPara(para_temp)
        sHtml = """<form id='alipaysubmit' name='alipaysubmit' action='%s_input_charset=%s' method='%s'  target="_blank">""" \
                        %( self.alipay_gateway_new, self.alipay_config['input_charset'].lower() , method)
        for k in para :
            sHtml += "<input type='hidden' name='%s' value='%s'/>" %(str(k), str(para[k]))
        sHtml = "%s<input type='submit' value='%s'></form>" %(sHtml , button_name)
        return sHtml

    def buildRequestUrl(self, para_temp):
        para = self.buildRequestPara(para_temp)
        data = "&%s" % urllib.urlencode(para)
        return self.alipay_gateway_new +'?'+ data

    def buildRequestHttp(self, para_temp) :
        sResult = ''
        request_data = self.buildRequestPara(para_temp)
        sResult = getHttpResponsePOST(self.alipay_gateway_new, self.alipay_config['cacert'],  request_data, self.alipay_config['input_charset'].lower() )
        return sResult

    def buildRequestHttpInFile(self, para_temp, file_para_name, file_name) :
        para = self.buildRequestPara(para_temp);
        para[file_para_name] = "@%s" % file_name

        sResult = getHttpResponsePOST(self.alipay_gateway_new,  self.alipay_config['cacert'],  para, self.alipay_config['input_charset'].lower());

        return sResult

    def query_timestamp(self) :
        url = "%sservice=query_timestamp&partner=%s&_input_charset=%s" %(self.alipay_gateway_new, self.alipay_config['partner'].lower(), self.alipay_config['input_charset'].lower() )
        encrypt_key = ""
        return encrypt_key
