import json

import requests
from flask import Blueprint, request, current_app

from exceptions import InvalidParam, ServerError


bp = Blueprint('weixin', __name__, url_prefix="/weixin")


@bp.get("/get_openid")
def get_openid():
    appid = current_app.config["WEIXIN"]["APPID"]
    secret = current_app.config["WEIXIN"]["SECRET"]
    code = request.args.get('code', None)
    current_app.logger.info(code)
    if code is None:
        raise InvalidParam(err_msg="code is None")
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&" \
        f"secret={secret}&js_code={code}&grant_type=authorization_code"
    rsp = requests.get(url)
    data = json.loads(rsp.text)
    current_app.logger.info(data)
    if "errcode" in data.keys():
        raise ServerError(
            f"weixin api respone: {data['errcode']} - {data['errmsg']}")
    return {
        "openid": data["openid"]
    }
