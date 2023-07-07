from flask import Blueprint

bp = Blueprint("alipay",__name__,static_folder='/alipay')

import alipay_api