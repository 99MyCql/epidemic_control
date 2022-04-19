import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import default_handler


def init_app(app : Flask):
    # 移除缺省的日志处理器
    app.logger.removeHandler(default_handler)

    # 配置新的日志处理器
    if app.config['LOG']['OUTPUT'] == "console":
        handler = logging.StreamHandler()
    elif app.config['LOG']['OUTPUT'] == "file":
        # 输出到文件，并按文件大小自动分割
        handler = RotatingFileHandler(
            os.path.join(app.config['LOG']['DIR'], "log.log"),
            maxBytes=app.config['LOG']['MAX_BYTES'],
            backupCount=10, encoding="UTF-8")
    else:
        raise Exception("配置文件中 LOG.OUTPUT 配置错误")

    # 配置输出格式
    formatter = logging.Formatter("[%(asctime)s][%(module)s:%(lineno)d]" \
        "[%(levelname)s] - %(message)s")
    handler.setFormatter(formatter)

    # 配置日志等级
    app.logger.setLevel(app.config['LOG']['LEVEL'])

    app.logger.addHandler(handler)
