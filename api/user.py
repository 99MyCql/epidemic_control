import json

from flask import Blueprint, current_app, session
from flask_restful import reqparse
import requests

from database import db
from models.user import User
from exceptions import ServerError


bp = Blueprint("user", __name__, url_prefix="/users")

login_parser = reqparse.RequestParser()
login_parser.add_argument("code", type=str, required=True, location="args")


@bp.get("/login")
def login():
    args = login_parser.parse_args()
    current_app.logger.debug(args)

    # 通过 code 获取 openid
    url = f"https://api.weixin.qq.com/sns/jscode2session?" \
        f"appid={current_app.config['WEIXIN_APPID']}&" \
        f"secret={current_app.config['WEIXIN_SECRET']}&" \
        f"js_code={args['code']}&grant_type=authorization_code"
    rsp = requests.get(url)
    data = json.loads(rsp.text)
    current_app.logger.info(data)
    if "errcode" in data.keys():
        raise ServerError(
            err_msg=f"weixin api respone: {data['errcode']} - {data['errmsg']}")

    # 根据 openid 查询用户，若不存在则创建这个用户
    u = User.query.filter_by(wx_openid=data["openid"]).first()
    current_app.logger.debug(u)
    if u is None:
        u = User(wx_openid=data["openid"])
        db.session.add(u)
        db.session.commit()

    # 保存用户到 session
    session["user_id"] = u.id

    return {
        "openid": data["openid"]
    }
