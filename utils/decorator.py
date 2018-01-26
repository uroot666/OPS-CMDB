# encoding: utf-8
# 用于登陆验证的装饰器

from functools import wraps
import json

from flask import session
from flask import redirect
from flask import request
from flask import flash

def login_required(func):
    @wraps(func)
    def required(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        elif session.get('user')['admin'] != 1:
            flash('只有管理员有权限访问此页面!', 'danger')
            return redirect('/')
        return func(*args, **kwargs)
    return required

def guest_login_required(func):
    @wraps(func)
    def required(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        return func(*args, **kwargs)
    return required