from functools import wraps

from flask import Blueprint, session, current_app
from flask_restful import reqparse, marshal, fields
from sqlalchemy import and_

from database import db
from models.organization import Organization
from models.member import Member, Role
import exceptions


bp = Blueprint("organization", __name__, url_prefix="/organizations")


# 判断组织是否存在
def check_org_exist(f):
    @wraps(f)
    def wrapper(org_id, *args, **kwargs):
        org = Organization.query.get(org_id)
        if org is None:
            raise exceptions.NotExist(err_msg="组织不存在")
        return f(org_id, *args, **kwargs)
    return wrapper


# 检查当前登录用户是否具有管理员权限
def check_admin_auth(f):
    @wraps(f)
    def wrapper(org_id, *args, **kwargs):
        m = Member.query.filter_by(organization_id=org_id, user_id=session["user_id"]).first()
        if m is None or m.role != Role.admin:
            raise exceptions.Unauthorized(err_msg="没有权限")
        return f(org_id, *args, **kwargs)
    return wrapper


create_req = reqparse.RequestParser()
create_req.add_argument("name", type=str, required=True)
create_req.add_argument("avatar_url", type=str)
create_req.add_argument("desc", type=str)
create_req.add_argument("contact", type=str)
create_req.add_argument("contact_phone", type=str)
create_req.add_argument("address", type=str)
create_req.add_argument("address_longitude", type=float)
create_req.add_argument("address_latitude", type=float)
create_req.add_argument("member_number_part", type=str)

# 创建组织
@bp.post("")
def create():
    args = create_req.parse_args()

    # 判断组织名称是否存在
    o = Organization.query.filter_by(name=args["name"]).first()
    if o is not None:
        raise exceptions.DuplicateField(err_msg="组织名称已存在")

    # 创建组织
    o = Organization(**args)
    db.session.add(o)
    db.session.commit()

    # 将当前登录用户设为管理员
    m = Member()
    m.user_id = session["user_id"]
    m.organization_id = o.id
    m.role = Role.admin
    db.session.add(m)
    db.session.commit()

    return {
        "id": o.id
    }


# 删除组织
@bp.delete("/<int:org_id>")
@check_org_exist
@check_admin_auth
def delete(org_id):
    # 删除组织内的所有成员
    members = Member.query.filter_by(organization_id=org_id).all()
    for m in members:
        db.session.delete(m)

    # 删除组织
    Organization.query.get(org_id).delete()
    db.session.commit()
    return {}


update_req = create_req.copy()

# 更新组织
@bp.put("/<int:org_id>")
@check_org_exist
@check_admin_auth
def update(org_id):
    args = update_req.parse_args()

    # 判断组织名称是否存在
    o = Organization.query.filter(
        and_(Organization.id!=org_id, Organization.name==args["name"])).first()
    if o is not None:
        raise exceptions.DuplicateField(err_msg="组织名称已存在")

    Organization.query.filter_by(id=org_id).update(args)
    db.session.commit()
    return {}


# 获取组织
@bp.get("/<int:org_id>")
def get(org_id):
    o = Organization.query.get(org_id)
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


create_member_req = reqparse.RequestParser()
create_member_req.add_argument("member_number", type=str, required=True)
create_member_req.add_argument("name", type=str)
create_member_req.add_argument("phone", type=str)
create_member_req.add_argument("family_members_count", type=int)
create_member_req.add_argument("family_others_name", type=str)

# 将自己（当前登录用户）加入到组织(org_id)中
@bp.post("/<int:org_id>/members")
@check_org_exist
def create_member(org_id):
    args = create_member_req.parse_args()

    # 判断成员编号是否已存在
    m = Member.query.filter_by(
        organization_id=org_id, member_number=args["member_number"]).first()
    if m is not None:
        raise exceptions.DuplicateField(err_msg="编号已存在")

    # 判断用户是否已加入
    m = Member.query.filter_by(organization_id=org_id, user_id=session["user_id"]).first()
    if m is not None:
        raise exceptions.AlreadyExist(err_msg="当前用户已加入该组织")

    # 新增成员
    m = Member(**args)
    m.organization_id = org_id
    m.user_id = session["user_id"]
    m.role = Role.common
    db.session.add(m)
    db.session.commit()
    return {}


# 获取组织中的成员列表
@bp.get("/<int:org_id>/members")
@check_org_exist
@check_admin_auth
def list_members(org_id):
    members = Member.query.filter_by(organization_id=org_id).all()
    members_dict = []
    for m in members:
        members_dict.append(marshal(m, {
            "id": fields.Integer,
            "member_number": fields.String,
            "user_id": fields.Integer,
            "role": fields.String(attribute=lambda x: x.role.name),
            "name": fields.String,
            "phone": fields.String,
            "family_members_count": fields.Integer,
            "family_others_name": fields.String,
            "create_time": fields.DateTime(dt_format="iso8601"),
            "update_time": fields.DateTime(dt_format="iso8601")
        }))
    return {"members": members_dict}


update_member_role_req = reqparse.RequestParser()
update_member_role_req.add_argument("role", type=str, required=True)

# 更新组织成员身份
@bp.put("/<int:org_id>/members/<int:mem_id>/role")
@check_org_exist
@check_admin_auth
def update_member_role(org_id, mem_id):
    args = update_member_role_req.parse_args()
    if not Role.has_key(args["role"]):
        raise exceptions.InvalidParam(err_msg=f"不存在身份：{args['role']}")

    m = Member.query.filter_by(id=mem_id).first()
    if m is None:
        raise exceptions.NotExist(err_msg="成员不存在")
    if m.user_id == session["user_id"]:
        raise exceptions.Forbidden(err_msg="不能修改自己的身份")

    m.role = Role[args["role"]]
    db.session.commit()
    return {}


# 删除组织成员
@bp.delete("/<int:org_id>/members/<int:mem_id>")
@check_org_exist
@check_admin_auth
def delete_member(org_id, mem_id):
    m = Member.query.filter_by(id=mem_id).first()
    if m is None:
        raise exceptions.NotExist(err_msg="成员不存在")
    if m.user_id == session["user_id"]:
        raise exceptions.Forbidden(err_msg="不能删除自己")

    db.session.delete(m)
    db.session.commit()
    return {}
