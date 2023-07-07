from flask import Blueprint

bp = Blueprint("cheak",__name__,static_folder='/cheak')

from . import cheak1,cheak2