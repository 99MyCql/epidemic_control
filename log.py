import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, has_request_context, session
from flask.logging import default_handler


# 注入请求信息
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.user_id = session.get('user_id', '')
        else:
            record.user_id = ""
        return super().format(record)


def init_app(app : Flask):
    # 移除缺省的日志处理器
    app.logger.removeHandler(default_handler)

    # 配置新的日志处理器
    handler = None
    if app.config['LOG_OUTPUT'] == "console":
        handler = logging.StreamHandler()
    elif app.config['LOG_OUTPUT'] == "file":
        # 输出到文件，并按文件大小自动分割
        handler = RotatingFileHandler(
            os.path.join(app.config['LOG_DIR'], "log.log"),
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=10, encoding="UTF-8")
    else:
        raise Exception("配置文件中 LOG.OUTPUT 配置错误")

    # 配置输出格式
    formatter = RequestFormatter("[%(asctime)s][%(module)s:%(lineno)d]" \
        "[%(levelname)s][user_id:%(user_id)s] - %(message)s")
    handler.setFormatter(formatter)

    # 配置日志等级
    app.logger.setLevel(app.config['LOG_LEVEL'])

    app.logger.addHandler(handler)
