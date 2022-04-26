from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def init_app(app : Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://" \
        f"{app.config['MYSQL_USERNAME']}:{app.config['MYSQL_PASSWORD']}" \
        f"@{app.config['MYSQL_HOST']}:{app.config['MYSQL_PORT']}" \
        f"/{app.config['MYSQL_DATABASE']}"
    db.init_app(app)
    migrate.init_app(app, db)
