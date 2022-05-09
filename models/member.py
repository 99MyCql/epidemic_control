from datetime import datetime
from email.policy import default
from enum import Enum

from database import db


class Role(Enum):
    common = 1 # 普通成员
    admin = 2 # 管理员

    @classmethod
    def has_key(cls, name):
        return name in cls._member_map_.keys()


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_number = db.Column(db.String(100), unique=True, index=True, comment="成员编号")
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.Enum(Role), default=Role.common, comment="角色，枚举类型。")
    name = db.Column(db.String(20), comment="姓名")
    phone = db.Column(db.String(20), comment="电话")
    family_members_count = db.Column(db.Integer, comment="家庭人数")
    family_others_name = db.Column(db.String(1000), comment="家庭其他成员姓名。多个姓名之间用逗号隔开，例如：'张三,李四'。")
    create_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="修改时间")

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self) -> str:
        return '{' + ', '.join(['%s:%s' % item for item in self.__dict__.items()]) + '}'