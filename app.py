#encoding=utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import json
import re

import model
import idc_model

app = Flask(__name__)
app.secret_key = "\xc5T|\xc9\x1b6\x8c\xef(\xc6\xfd\x86S\x82b\x19)\xcdg\x1c3Mf\x93z|Bk"
#首页
@app.route('/')
def index():
    if session.get('user'):
        return redirect('/users/')
    return render_template('index.html')

# 登录并跳转
@app.route('/login/', methods=["POST"])
def login():
    if session.get('user'):
        return redirect('/users/')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    user = model.validate_login(username, password)
    if user:
        session['user'] = user
        return redirect('/users/')
    else:
        return render_template('index.html', username=username,  error='用户或密码错误')

# 显示所有用户信息
@app.route('/users/')
def users():
    if session.get('user') is None:
        return redirect('/')
    user_all = model.get_users()   
    return render_template("users.html", user_all=user_all)

# 添加用户界面
@app.route('/user/add/')
def user_add():
    if session.get('user') is None:
        return redirect('/')
    return render_template('user_create.html')

# 保存添加用户
@app.route('/user/create/', methods=["POST"])
def user_create():
    if session.get('user') is None:
        return redirect('/')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    email = request.form.get('email', '')
    age = request.form.get('age', '')
    if username == '' or password == '' or age == '':
        return json.dumps({'code' : 400, 'error' : 'error'})

    else:
        model.user_create(username, password, int(age), email)
        return json.dumps({'code' : 200})


# 删除用户
@app.route('/user/delete/')
def userdel():
    if session.get('user') is None:
        return redirect('/')
    id = int(request.args.get('id', ''))
    jud = model.user_del(id)
    user_all = model.get_users()
    if jud:
        return redirect('/users/')
    else:
        return render_template('users.html', error='error', user_all=user_all)

# 修改用户
@app.route('/user/view/')
def user_view():
    if session.get('user') is None:
        return redirect('/')
    user = model.get_user_by_id(request.args.get('id', 0))
    return render_template('user_view.html', uid=user.get("uid"), username=user.get("username"), age=user.get("age"), email=user.get("email"))

# 保存修改的用户信息
@app.route('/user/view_save/')
def user_view_save():
    if session.get('user') is None:
        return redirect('/')
    uid = int(request.args.get('uid'))
    username = request.args.get('username')
    age = request.args.get('age')
    email = request.args.get('email')
    ok = model.user_edit_jud(uid, username, age)
    if ok:
        model.user_edit_save(uid, username, email, age)
        return redirect('/users/')
    else:
        return render_template('user_view.html', uid=uid, username=username, age=age, email=email, error=error)


#查询分析日志的结果表单页面
@app.route('/log/')
def log():
    if session.get('user') is None:
        return redirect('/')
    topn = request.args.get('topn', 10)
    topn = int(topn) if str(topn).isdigit() else 10
    access_file_path = "access.log"
    result = model.gethtml(access_file_path, topn)
    return  render_template('log.html', logs=result)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route("/static/")
def test():
    return render_template('index.html')


############################# 资产管理 #############################
@app.route("/asset/")
def asset_index():
    if session.get('user') is None:
        return redirect('/')
    return render_template('asset.html')

@app.route("/asset/list/")
def asset_list():
    assets = idc_model.get_asset()
    return json.dumps({"data": assets})

@app.route("/idc_list/")
def idc_list():
    engineroom_all = idc_model.engineroom_list()
    return render_template('idc_list.html', engineroom_all=engineroom_all)

@app.route("/idc/add/")
def idc_add():
    return render_template('idc_create.html')

@app.route("/idc/add_save/", methods=["POST"])
def idc_add_save():
    idcname = request.form.get('idcname', '')
    area = request.form.get('area', '')
    ip_segment = request.form.get('ip_segment', '')
    machine_number = request.form.get('machine_number', '')
    if idcname == '' or area == '' or ip_segment == '' or machine_number == '':
        return json.dumps({'code' : 400})
    else:
        idc_model.idc_add_save(idcname, area, ip_segment, int(machine_number))
        return json.dumps({'code':200})

@app.route("/idc/view/")
def idc_view():
    idcid = int(request.args.get('id'))
    idc_tails = idc_model.idc_tails_get(idcid)
    idcname = idc_tails.get("idcname")
    area = idc_tails.get("area")
    ip_segment = idc_tails.get("ip_segment")
    machine_number = idc_tails.get("engineroom_number")
    return render_template('idc_view.html', idcid=idcid, idcname=idcname, ip_segment=ip_segment, area=area, machine_number=machine_number)

@app.route("/idc/view_save/")
def idc_view_save():
    idcid = int(request.args.get('idcid'))
    idcname = request.args.get('idcname')
    area = request.args.get('area')
    ip_segment = request.args.get("ip_segment")
    machine_number = int(request.args.get('machine_number'))
    idc_model.idc_view_save(idcid, idcname, area, ip_segment, machine_number)
    return redirect("/idc_list/")

@app.route("/idc/delete/")
def idc_delete():
    id = request.args.get('id', '0')
    if re.match(r'\d+', id):
        stu = idc_model.idcroom_delete(int(id))
        return redirect('/idc_list/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
