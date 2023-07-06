import alipay_core_function
import alipay_md5_function
import urllib

class AlipaySubmit:
    alipay_config = ""
    alipay_gateway_new = 'https://mapi.alipay.com/gateway.do?'

    def __init__(self, alipay_config) :
        self.alipay_config = alipay_config

    def AlipaySubmit(self, alipay_config) :
        self.__init__(alipay_config)

    def buildRequestMysign(self, para_sort) :
        keys = alipay_core_function.argSort(para_sort)
        prestr = alipay_core_function.createLinkstring(para_sort, keys)
        print ("==%s=%s==" %(para_sort, prestr))
        if self.alipay_config['sign_type'].upper()  == 'MD5':
            mysign = alipay_md5_function.md5Sign(prestr, self.alipay_config['key'])
        else :
            mysign = ""
        return mysign

    def buildRequestPara(self, para_temp) :
        para_sort = alipay_core_function.paraFilter(para_temp)
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
        sResult = alipay_core_function.getHttpResponsePOST(self.alipay_gateway_new, self.alipay_config['cacert'],  request_data, self.alipay_config['input_charset'].lower() )
        return sResult

    def buildRequestHttpInFile(self, para_temp, file_para_name, file_name) :
        para = self.buildRequestPara(para_temp);
        para[file_para_name] = "@%s" % file_name

        sResult = alipay_core_function.getHttpResponsePOST(self.alipay_gateway_new,  self.alipay_config['cacert'],  para, self.alipay_config['input_charset'].lower());

        return sResult

    def query_timestamp(self) :
        url = "%sservice=query_timestamp&partner=%s&_input_charset=%s" %(self.alipay_gateway_new, self.alipay_config['partner'].lower(), self.alipay_config['input_charset'].lower() )
        encrypt_key = ""
        return encrypt_key
