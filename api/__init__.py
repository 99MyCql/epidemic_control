from flask import Blueprint, current_app
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from . import weixin, user
from exceptions import APIException, UnknownError, DatabaseError


bp = Blueprint('api', __name__, url_prefix="/api")
bp.register_blueprint(weixin.bp)
bp.register_blueprint(user.bp)


# 异常处理
@bp.errorhandler(Exception)
def error_handler(e):
    current_app.logger.error(e)
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        return APIException(code=e.code, err_code=e.code*1000,
            err_name=e.name, err_msg=e.description)
    if isinstance(e, SQLAlchemyError):
        return DatabaseError(err_msg=e._message())
    return UnknownError(err_msg=str(e))
