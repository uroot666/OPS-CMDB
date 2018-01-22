# encoding: utf-8
# 用于登陆验证的装饰器

from functools import wraps
import json

from flask import session
from flask import redirect
from flask import request

def login_required(func):
    @wraps(func)
    def required(*args, **kwargs):
        if session.get('user') is None:
            if request.is_xhr:
                return json.dumps({"code": 401, "error": ''})
            return redirect('/')
        return func(*args, **kwargs)
    return required