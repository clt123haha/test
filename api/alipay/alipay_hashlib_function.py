import hashlib

def md5Sign(prestr, key) :
    prestr = "%s%s" % (prestr, key)
    m1 = hashlib.md5.new()
    m1.update(prestr) 
    return m1.hexdigest()

def md5Verify( prestr, sign, key) :
    prestr = "%s%s" % (prestr, key)
    m1 = hashlib.md5.new()
    m1.update(prestr) 
    mysgin = m1.hexdigest()
    if mysgin == sign :
        return True
    else :
        return False

def md5my_token(prestr, key):
    prestr = "%s%s" % (prestr, key)
    m1 = hashlib.md5.new()
    m1.update(prestr) 
    return m1.hexdigest()