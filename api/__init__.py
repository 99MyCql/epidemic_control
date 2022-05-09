from flask import Blueprint, Response, current_app, session, request, after_this_request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from . import user, organization
from exceptions import APIException, UnknownError, DatabaseError, NotLogin


bp = Blueprint('api', __name__, url_prefix="/api")
bp.register_blueprint(user.bp)
bp.register_blueprint(organization.bp)


# 异常处理
@bp.errorhandler(Exception)
def error_handler(e):
    current_app.logger.exception(e)
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        return APIException(code=e.code, err_code=e.code*1000,
            err_name=e.name, err_msg=e.description)
    if isinstance(e, SQLAlchemyError):
        return DatabaseError(err_msg=e._message())
    return UnknownError(err_msg=str(e))


# 打印请求信息
@bp.before_request
def log_request_info():
    current_app.logger.info(f"{request.remote_addr} {request.method} {request.url.replace(request.host_url, '/')} {request.data}")
    # 打印响应信息
    @after_this_request
    def log_rsp_info(rsp : Response):
        current_app.logger.info(f"rsp: {rsp.data}")
        return rsp


# 判断是否登录
@bp.before_request
def is_login():
    # 判断session是否超时
    if not request.path.endswith("/login") and session.get("user_id") is None:
        raise NotLogin()
    return None
