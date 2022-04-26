from datetime import datetime

from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wx_openid = db.Column(db.String(60), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")

    def __init__(self, wx_openid):
        self.wx_openid = wx_openid

    def __str__(self) -> str:
        return '{' + ', '.join(['%s:%s' % item for item in self.__dict__.items()]) + '}'
