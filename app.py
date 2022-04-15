import json

import yaml
import requests
from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def index():
    return "hello world!"


@app.route("/api/weixin/get_openid", methods=['GET'])
def get_openid():
    appid = app.config["WEIXIN"]["APPID"]
    secret = app.config["WEIXIN"]["SECRET"]
    code = request.args.get('code')
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code"
    rsp = requests.get(url)
    data = json.loads(rsp.text)
    app.logger.debug(data)
    return {
        "openid": data["openid"]
    }


def read_yaml(path):
    with open(path, 'rb') as f:
        y = yaml.load(f.read(), Loader=yaml.FullLoader)
    return y


if __name__ == "__main__":
    app.config.update(read_yaml('config.yaml'))
    app.run(
        host=app.config["SERVER"]["HOST"],
        port=app.config["SERVER"]["PORT"],
        debug=True,
        ssl_context=(
            app.config["SSL"]["CERT"],
            app.config["SSL"]["KEY"]
        )
    )
