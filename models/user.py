from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wx_openid = db.Column(db.String(80), unique=True)

    def __init__(self, wx_openid):
        self.wx_openid = wx_openid
