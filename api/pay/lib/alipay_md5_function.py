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