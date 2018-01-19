#encoding: utf-8

from restapi import bp
from restapi import model

from flask import render_template
from flask import request

import json

@bp.route('/help/')
def help():
    rt = model.help()
    return render_template('restapi/help.html')

@bp.route('/users/', methods=['GET', 'PUT', 'POST', 'DELETE'])
@bp.route('/users/<pkey>/', methods=['GET', 'PUT', 'POST', 'DELETE'])
def users(pkey=None):
    print(request.json)
    if request.method == 'GET':
        print('GET')
        if pkey is None:
            print('get all')
        else:
            print('get, %s' % pkey)
    elif request.method == 'PUT':
        print('PUT')
        print(pkey)
        print(request.form)
    elif request.method == 'POST':
        print('POST')
        print(pkey)
        print(request.form)
    elif request.method == 'DELETE':
        print('DELETE')
        print(pkey)
    return ''