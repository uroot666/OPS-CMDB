#encoding=UTF-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import model

app = Flask(__name__)

#首页
@app.route('/')
def index():
    return render_template('index.html')

#登录，登录成功跳转到'/users/'
@app.route('/login/')
def login():
    username=''
    password=''
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    user = model.validate_login(username, password)
    if user:
        return redirect('/users/')
    else:
        return render_template('index.html', username=username,  error='username of password for error')

#显示所有用户信息
@app.route('/users/')
def users():
    user_all = model.get_users()
    print(user_all)    
    return render_template("users.html", user_all=user_all)

#添加用户信息表单页面
@app.route('/users/add/')
def user_add():
    return render_template('user_create.html')

#获取要添加的用户信息，并添加到json文件中
@app.route('/users/create/')
def user_create():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    if username == '' or password == '':
        return 'user create error'
    else:
        model.user_create(username, password)
        return 'user create %s yes' % username

#查询分析日志的结果表单页面
@app.route('/log/')
def log():
    topn = request.args.get('topn', 10)
    topn = int(topn) if str(topn).isdigit() else 10
    access_file_path = "access.log"
    result = model.gethtml(access_file_path, topn)
    return  render_template('log.html', logs=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
