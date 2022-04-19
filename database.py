from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def init_app(app : Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://" \
        f"{app.config['MYSQL']['USERNAME']}:{app.config['MYSQL']['PASSWORD']}" \
        f"@{app.config['MYSQL']['HOST']}:{app.config['MYSQL']['PORT']}" \
        f"/{app.config['MYSQL']['DATABASE']}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # 关闭对模型修改的监控
    app.config["SQLALCHEMY_ECHO"] = True # 执行时显示SQL语句
    db.init_app(app)
    migrate.init_app(app, db)
