from flask import Flask

import api
import database
import log


app = Flask(__name__)
app.config.from_pyfile("config.py") # 默认配置文件
app.config.from_envvar("CONFIG_FILE", silent=True) # 重载的配置文件，通过环境变量 CONFIG_FILE 导入（可不设）
log.init_app(app)
database.init_app(app)
app.register_blueprint(api.bp) # 注册蓝图（注册路由）


@app.route("/")
def index():
    app.logger.info("hello world!")
    return "hello world!"


if __name__ == "__main__":
    app.run(debug=True)
