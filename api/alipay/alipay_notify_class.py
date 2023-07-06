import alipay_core_function
import alipay_md5_function
import utils

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
        if len(request_data) ==0 :
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

        para_filter = alipay_core_function.paraFilter(para_temp)

        keys = alipay_core_function.argSort(para_filter)

        prestr = alipay_core_function.createLinkstring(para_filter, keys)
        
        isSgin = False
        if self.alipay_config['sign_type'].upper() == 'MD5':
            isSgin = alipay_md5_function.md5Verify(prestr, sign, self.alipay_config['key'])

        elif self.alipay_config['sign_type'].upper() == 'RSA':
            pass
        else :
            isSgin = False
        return isSgin

    def getSignVeryfy2(self, out_trade_no, sign):
        return alipay_md5_function.md5Verify(out_trade_no, sign, self.alipay_config['key'] )

    def getResponse(self, notify_id) :
        transport = self.alipay_config['transport'].strip().lower()
        partner = self.alipay_config['partner'].strip()
        veryfy_url = ''
        
        if transport == 'https' :
            veryfy_url = self.https_verify_url
        else :
            veryfy_url = self.http_verify_url
        
        veryfy_url = "%spartner=%s&notify_id=%s" %(veryfy_url, partner, notify_id)
        responseTxt = alipay_core_function.getHttpResponseGET(veryfy_url, self.alipay_config['cacert'])
        
        return responseTxt