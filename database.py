from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_app(app : Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://" \
        "{app.config['MYSQL']['USERNAME']}:{app.config['MYSQL']['PASSWORD']}" \
        "@{app.config['MYSQL']['HOST']}:{app.config['MYSQL']['PORT']}" \
        "/{app.config['MYSQL']['DATABASE']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
    global db
    db.init_app(app)
