#encoding: utf-8

from flask import Flask

app = Flask(__name__)
app.secret_key = "\xc5T|\xc9\x1b6\x8c\xef(\xc6\xfd\x86S\x82b\x19)\xcdg\x1c3Mf\x93z|Bk"

from cmdb import views
from restapi import bp as restapi_bp
app.register_blueprint(restapi_bp)