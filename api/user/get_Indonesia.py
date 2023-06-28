import base64

from utils.tool import generate_captcha_image
from ..user import bp

@bp.route('/get_Indonesia')
def get_Indonesia():
    file_name = generate_captcha_image()
    with open(file_name, 'rb') as f:
        res = base64.b64encode(f.read())
    return res