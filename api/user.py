from flask import Blueprint, current_app
from flask_restful import reqparse

from database import db
from models.user import User


bp = Blueprint("user", __name__, url_prefix="/user")

create_parser = reqparse.RequestParser()
create_parser.add_argument("wx_openid", type=str)


@bp.post("/create")
def create():
    args = create_parser.parse_args()
    current_app.logger.info(args)
    db.session.add(User(wx_openid=args["wx_openid"]))
    db.session.commit()
    return {}
