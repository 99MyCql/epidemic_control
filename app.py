from flask import Flask
from werkzeug.exceptions import HTTPException

import api
import database
import log
from exceptions import APIException, ServerError, UnknownError
from utils import read_yaml


app = Flask(__name__)
app.config.update(read_yaml('config.yaml'))
log.init_app(app)
database.init_app(app)
app.register_blueprint(api.bp) # 注册蓝图（注册路由）


# 异常处理
@app.errorhandler(Exception)
def framework_error(e):
    app.logger.error(e)
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        return ServerError(msg=e.description)
    else:
        return UnknownError(msg=str(e))


@app.route("/")
def index():
    app.logger.info("hello world!")
    return "hello world!"


if __name__ == "__main__":
    app.run(
        host=app.config["SERVER"]["HOST"],
        port=app.config["SERVER"]["PORT"],
        debug=True
    )
