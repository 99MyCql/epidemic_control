from flask import Flask

import api
import database
import log
from utils import read_yaml


app = Flask(__name__)
app.config.update(read_yaml('config.yaml'))
log.init_app(app)
database.init_app(app)
app.register_blueprint(api.bp) # 注册蓝图（注册路由）


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
