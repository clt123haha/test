from flask import  Blueprint
#从Flask导入Blueprint类，实例化这个类就获得了我们的蓝本对象。
bp = Blueprint("user", __name__, url_prefix="/user")
#构造方法中的第一个参数是蓝本的名称；第二个参数是包或模块的名称，我们可以使用__name__变量
from . import history,login,reqister

from . import block,IdentityAuthenticate,mobile_text,reqister,history,login,get_Indonesia


