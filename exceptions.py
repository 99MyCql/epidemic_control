import json

from werkzeug.exceptions import HTTPException


"""自定义异常处理类

处理请求时抛出该异常，会被flask处理，并响应json格式的错误信息
"""
class APIException(HTTPException):
    code = 500 # HTTP状态码
    err_code = 500000 # 自定义的错误码（若HTTP状态码中存在相似错误，则默认code*1000）
    err_name = "Server Error" # 错误码说明
    err_msg = "" # 错误信息

    def __init__(self, code=None, err_code=None, err_name=None, err_msg=""):
        if code:
            self.code = code
        if err_code:
            self.err_code = err_code
        if err_name:
            self.err_name = err_name
        self.err_msg = err_msg
        super(APIException, self).__init__(err_msg, None)

    def get_body(self, environ=None, scope=None):
        return json.dumps({
            "err_code": self.err_code,
            "err_name": self.err_name,
            "err_msg": self.err_msg
        })

    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json')]

    def __str__(self) -> str:
        return f"{self.code} {self.err_code} {self.err_name}: {self.err_msg}"


class BadRequest(APIException):
    code = 400
    err_code = 400000
    err_name = "Bad Request"


class InvalidParam(APIException):
    code = 400
    err_code = 400001
    err_name = "Invalid Parameter"


class ServerError(APIException):
    code = 500
    err_code = 500000
    err_name = "Server Error"


class UnknownError(APIException):
    code = 500
    err_code = 500001
    err_name = "Unknown Error"


class DatabaseError(APIException):
    code = 500
    err_code = 500002
    err_name = "Database Error"
