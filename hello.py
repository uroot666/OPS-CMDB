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

# 登录并跳转
@app.route('/login/')
def login():
    username=''
    password=''
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    user = model.validate_login(username, password)
    print(user)
    if user:
        return redirect('/users/')
    else:
        return render_template('index.html', username=username,  error='username of password for error')

# 显示所有用户信息
@app.route('/users/')
def users():
    user_all = model.get_users()   
    return render_template("users.html", user_all=user_all)

# 添加用户界面
@app.route('/users/add/')
def user_add():
    return render_template('user_create.html')

# 保存添加用户
@app.route('/users/create/')
def user_create():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    if username == '' or password == '':
        return 'user create error'
    else:
        model.user_create(username, password)
        user_all = model.get_users()
        return render_template('users.html', create_username=username, user_all=user_all)

# 删除用户
@app.route('/user/delete/')
def userdel():
    id = int(request.args.get('id', ''))
    code, username = model.user_del(id)
    user_all = model.get_users()
    if code:
        return render_template('users.html', username=username, user_all=user_all)
    else:
        return render_template('users.html', error='error', username=username, user_all=user_all)

# 修改用户
@app.route('/user/view/')
def user_view():
    id = request.args.get('id')
    username = request.args.get('username')
    return render_template('user_view.html', id=id, username=username)

# 保存修改的用户信息
@app.route('/user/view_save/')
def user_view_save():
    id = int(request.args.get('id'))
    username = request.args.get('username')
    password = request.args.get('password')
    status = model.userEditSave(id, username, password)
    user_all = model.get_users()
    if status:
        return render_template('users.html', user_all=user_all)
    else:
        return "edit %s error" % username


#查询分析日志的结果表单页面
@app.route('/log/')
def log():
    topn = request.args.get('topn', 10)
    topn = int(topn) if str(topn).isdigit() else 10
    access_file_path = "access.log"
    result = model.gethtml(access_file_path, topn)
    return  render_template('log.html', logs=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
