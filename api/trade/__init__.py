from flask import Blueprint

bp = Blueprint("trade", __name__, url_prefix="/trade")

from . import  get_transaction,put_new_transaction