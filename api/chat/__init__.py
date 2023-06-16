from flask import Blueprint

bp = Blueprint("chat",__name__,static_folder='/chat')

from ..chat import sendmessage