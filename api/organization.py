from flask import Blueprint, session
from flask_restful import reqparse, marshal, fields

from database import db
from models.organization import Member, Organization
from exceptions import AlreadyExist, DuplicateField, NotExist


bp = Blueprint("organization", __name__, url_prefix="/organization")

create_parser = reqparse.RequestParser()
create_parser.add_argument("type", type=str, default="1")
create_parser.add_argument("name", type=str, required=True)
create_parser.add_argument("avatar_url", type=str)
create_parser.add_argument("desc", type=str)
create_parser.add_argument("contact", type=str)
create_parser.add_argument("contact_phone", type=str)
create_parser.add_argument("address", type=str)
create_parser.add_argument("address_longitude", type=float)
create_parser.add_argument("address_latitude", type=float)
create_parser.add_argument("member_number_part", type=str)


@bp.post("/create")
def create():
    args = create_parser.parse_args()

    # 判断组织名称是否存在
    o = Organization.query.filter_by(name=args["name"]).first()
    if o is not None:
        raise DuplicateField(err_msg="组织名称已存在")

    # 创建组织
    o = Organization(**args)
    db.session.add(o)
    db.session.commit()

    # 将当前用户设为管理员
    m = Member()
    m.user_id = session["user_id"]
    m.organization_id = o.id
    m.role = "2"
    db.session.add(m)
    db.session.commit()

    return {
        "id": o.id
    }


@bp.get("/get/<int:id>")
def get(id):
    o = Organization.query.get(id)
    if o is None:
        return {}
    return marshal(o, {
        "name": fields.String,
        "avatar_url": fields.String,
        "desc": fields.String,
        "contact": fields.String,
        "contact_phone": fields.String,
        "address": fields.String,
        "address_longitude": fields.Float,
        "address_latitude": fields.Float,
        "member_number_part": fields.String,
        "create_time": fields.DateTime(dt_format="iso8601"),
        "update_time": fields.DateTime(dt_format="iso8601")
    })


create_member_parser = reqparse.RequestParser()
create_member_parser.add_argument("member_number", type=str, required=True)
create_member_parser.add_argument("organization_id", type=int, required=True)
create_member_parser.add_argument("role", type=str, default="1")
create_member_parser.add_argument("name", type=str)
create_member_parser.add_argument("phone", type=str)
create_member_parser.add_argument("family_members_count", type=int)
create_member_parser.add_argument("family_others_name", type=str)


@bp.post("/create_member")
def create_member():
    args = create_member_parser.parse_args()

    # 判断组织是否存在
    o = Organization.query.get(args["organization_id"])
    if o is None:
        raise NotExist(err_msg="组织ID不存在")

    # 判断成员编号是否已存在
    m = Member.query.filter_by(member_number=args["member_number"]).first()
    if m is not None:
        raise DuplicateField(err_msg="编号已存在")

    # 判断用户是否已加入
    m = Member.query.filter_by(organization_id=args["organization_id"], user_id=session["user_id"]).first()
    if m is not None:
        raise AlreadyExist(err_msg="用户已加入该组织")

    # 新增成员
    m = Member(**args)
    m.user_id = session["user_id"]
    db.session.add(m)
    db.session.commit()
    return {}
