#encoding=UTF-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import model

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
    username=''
    password=''
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    user = model.validate_login(username, password)
    if user:
        return redirect('/log/')
    else:
        return render_template('index.html', username=username,  error='username of password for error')

@app.route('/log/')
def log():
    topn = request.args.get('topn', 10)
    topn = int(topn) if str(topn).isdigit() else 10
    access_file_path = "access.log"
    result = model.gethtml(access_file_path, topn)
    return  render_template('log.html', logs=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
