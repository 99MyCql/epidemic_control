from datetime import datetime

from database import db


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), comment="类型。1代表社区，2代表学校。")
    name = db.Column(db.String(60), unique=True, index=True, comment="名称")
    desc = db.Column(db.Text, comment="简介")
    contact = db.Column(db.String(20), comment="联系人")
    contact_phone = db.Column(db.String(20), comment="联系人电话")
    address = db.Column(db.String(100), comment="地址（省市县+详细地址）")
    address_longitude = db.Column(db.Float, comment="地址（经度）")
    address_latitude = db.Column(db.Float, comment="地址（维度）")
    member_number_example = db.Column(db.String(100), comment="成员编号样例")
    member_number_part = db.Column(db.String(20), comment="成员编号组成部分。1代表楼栋号，2代表单元号，3代表门牌号。若值为 '1,2,3' 表示成员编号由 楼栋号、单元号、门牌号 组成")
    create_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="修改时间")

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self) -> str:
        return '{' + ', '.join(['%s:%s' % item for item in self.__dict__.items()]) + '}'


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100), comment="编号")
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String(20), comment="角色。1代表普通成员，2代表管理员。")
    name = db.Column(db.String(20), comment="姓名")
    phone = db.Column(db.String(20), comment="电话")
    family_number = db.Column(db.Integer, comment="家庭人数")
    family_others_name = db.Column(db.String(1000), comment="家庭其他成员姓名。多个姓名之间用逗号隔开，例如：'张三,李四'。")
    create_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="修改时间")

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self) -> str:
        return '{' + ', '.join(['%s:%s' % item for item in self.__dict__.items()]) + '}'
