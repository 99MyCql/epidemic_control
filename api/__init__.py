from flask import Blueprint, current_app

from . import weixin


bp = Blueprint('api', __name__, url_prefix="/api")
bp.register_blueprint(weixin.bp, url_prefix="/weixin")
