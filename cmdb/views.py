#encoding=utf-8

# from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import datetime
import os
import json
import re

from . import model

from cmdb import app

# app = Flask(__name__)
# app.secret_key = "\xc5T|\xc9\x1b6\x8c\xef(\xc6\xfd\x86S\x82b\x19)\xcdg\x1c3Mf\x93z|Bk"
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
    user = model.User.validate_login(username, password)
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
    user_all = model.User.get_list()   
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
        user = model.User('', username, password, int(age), email)
        user.save()
        return json.dumps({'code' : 200})


# 删除用户
@app.route('/user/delete/')
def userdel():
    if session.get('user') is None:
        return redirect('/')
    id = int(request.args.get('id', ''))
    jud = model.User.delete_by_key(id, 'id')
    user_all = model.User.get_list()
    if jud:
        return redirect('/users/')
    else:
        return render_template('users.html', error='error', user_all=user_all)

# 修改用户
@app.route('/user/view/')
def user_view():
    if session.get('user') is None:
        return redirect('/')
    user = model.User.get_user_by_id(request.args.get('id', 0))
    return render_template('user_view.html', uid=user.get("uid"), username=user.get("username"), age=user.get("age"), email=user.get("email"))

# 保存修改的用户信息
@app.route('/user/view_save/', methods=["POST"])
def user_view_save():
    if session.get('user') is None:
        return redirect('/')
    uid = int(request.form.get('uid'))
    username = request.form.get('username')
    age = request.form.get('age')
    email = request.form.get('email')
    user = model.User(uid, username, '', age, email)
    ok = model.User.validate_user_modify(uid, username, age)
    if ok:
        user.user_edit_save()
        return redirect('/users/')
    else:
        return render_template('user_view.html', uid=uid, username=username, age=age, email=email, error='error')

# 修改用户密码
@app.route('/user/set/password/', methods=['POST'])
def user_set_password_view():
    if session.get('user') is None:
        return redirect('/')
    uid = request.form.get('uid')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    if model.User.judgment_old_password(uid, old_password):
        user = model.User(uid, '', new_password, '', '')
        user.set_password()
        return json.dumps({"code":200})
    else:
        return json.dumps({"code":400})


# 上传文件处理
@app.route('/upload/', methods=['POST'])
def upload():
    ALLOWED = set(['log', 'py']) # 允许后缀
    upload_dir = os.path.join(app.config['basedir'], 'temp')  #存储路径
    file = request.files['upload']  # 上传文件数据
    if file:
        result = model.upload(file, ALLOWED, upload_dir)
        print(result)
    return redirect('/log/')

#查询分析日志的结果表单页面
@app.route('/log/')
def log_index():
    if session.get('user') is None:
        return redirect('/')
    # top = request.form
    topn = request.args.get('topn', '')
    return render_template('log.html', topn = topn)

# 返回分析日志的信息给页面
@app.route('/log/list/')
def log():
    if session.get('user') is None:
        return redirect('/')
    topn = request.args.get('topn', 10)
    topn = int(topn) if str(topn).isdigit() else 10
    result = model.get_log_analysis(topn)
    # result = model.gethtml('access.log', topn)
    return json.dumps({"data" : result})

# 退出登录
@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

# 返回静态资源的默认页面
@app.route("/static/")
def test():
    return render_template('index.html')


############################# 资产管理 #############################

# 返回资产管理页面
@app.route("/asset/")
def asset_index():
    if session.get('user') is None:
        return redirect('/')
    # 查询出所有机房的列表，返回到资产管理页面
    engineroom_all = model.engineroom_list()
    return render_template('asset.html', engineroom_all=engineroom_all)

# 返回资产信息
@app.route("/asset/list/")
def asset_list():
    assets = model.get_asset()
    return json.dumps({"data": assets})

# 保存添加资产信息
@app.route("/asset/save/", methods=["POST"])
def asset_save():
    as_list = []
    for key in request.form:
        as_list.append(request.form.get(key))
    asset_save_value = model.asset_save(tuple(as_list[1:]))
    return json.dumps({"code" : 200})

# 修改资产
@app.route("/asset/view/")
def asset_view():
    aid = request.args.get('id', 0)
    view_asset_value = model.get_asset_by_id(int(aid))
    return json.dumps(view_asset_value)

# 保存修改后的资产信息
@app.route("/asset/update/", methods=["POST"])
def asset_update():
    au_list = []
    for key in request.form:
        au_list.append(request.form.get(key))
    au_list = au_list[1:] + [au_list[0]]
    asset_update_value = model.asset_update(tuple(au_list))
    return json.dumps({"code" : 200})

# 删除资产
@app.route("/asset/delete/", methods=["POST"])
def asset_delete():
    aid = request.form.get("id")
    if aid:
        model.asset_delete(int(aid))
        return json.dumps({"code" : 200})


####################### 机房信息管理 #########################
# 机房信息页面
@app.route("/idc_list/")
def idc_list():
    engineroom_all = model.engineroom_list()
    return render_template('idc_list.html', engineroom_all=engineroom_all)

# 返回机房添加页面
@app.route("/idc/add/")
def idc_add():
    return render_template('idc_create.html')

# 保存添加的机房
@app.route("/idc/add_save/", methods=["POST"])
def idc_add_save():
    idcname = request.form.get('idcname', '')
    area = request.form.get('area', '')
    ip_segment = request.form.get('ip_segment', '')
    machine_number = request.form.get('machine_number', '')
    if idcname == '' or area == '' or ip_segment == '' or machine_number == '':
        return json.dumps({'code' : 400})
    else:
        model.idc_add_save(idcname, area, ip_segment, int(machine_number))
        return json.dumps({'code':200})

# 返回机房修改页面
@app.route("/idc/view/")
def idc_view():
    idcid = int(request.args.get('id'))
    idc_tails = model.idc_tails_get(idcid)
    idcname = idc_tails.get("idcname")
    area = idc_tails.get("area")
    ip_segment = idc_tails.get("ip_segment")
    machine_number = idc_tails.get("engineroom_number")
    return render_template('idc_view.html', idcid=idcid, idcname=idcname, ip_segment=ip_segment, area=area, machine_number=machine_number)

# 将机房修改信息保存到数据库
@app.route("/idc/view_save/")
def idc_view_save():
    idcid = int(request.args.get('idcid'))
    idcname = request.args.get('idcname')
    area = request.args.get('area')
    ip_segment = request.args.get("ip_segment")
    machine_number = int(request.args.get('machine_number'))
    model.idc_view_save(idcid, idcname, area, ip_segment, machine_number)
    return redirect("/idc_list/")

#删除机房
@app.route("/idc/delete/")
def idc_delete():
    id = request.args.get('id', '0')
    if re.match(r'\d+', id):
        model.idcroom_delete(int(id))
        return redirect('/idc_list/')

####################### agent http接口 ##########################
# 将agent发回的数据存储到数据库
@app.route('/monitor/host/create/', methods=['POST'])
def monitor_host_create():
    req = request.form
    # ip = request.form.get('ip', '')
    # cpu = request.form.get('cpu', '')
    # mem = request.form.get('mem', '')
    # disk = request.form.get('disk', '')
    # m_time = request.form.get('m_time', '')
    # model.monitor_host_create(ip, cpu, mem, disk, m_time)
    model.monitor_host_create(req)
    return json.dumps({'code' : 200})


# 返回资源状态信息
@app.route('/monitor/host/list/')
def monitor_host_list():
    id = request.args.get('id')
    asset = model.get_asset_by_id(id)
    ip = asset.get('ip', '')
    result = model.monitor_host_list(ip)
    return json.dumps({'code':200, 'result':result})

# 返回告警日志页面
@app.route('/moitor/log/')
def moitor_log_index():
    if session.get('user') is None:
        return redirect('/')
    return render_template('moitor_log.html')

# 查询出告警日志，然会给告警页面
@app.route('/moitor/log/list/')
def moitor_log_list():
    moitor_log = model.get_moitor_log()
    return json.dumps({"data" : moitor_log})

# 删除告警日志
@app.route('/moitor/log/delete/', methods = ['POST'])
def monitor_log_delete():
    id = request.form.get('id', '')
    req = model.monitor_log_delete(id)
    return json.dumps(req)

@app.route('/host/ssh/', methods=['POST'])
def host_ssh():
    host_id = int(request.form.get('id', ''))
    system_user = request.form.get('system_user', '')
    system_password = request.form.get('system_password', '')
    ssh_command = request.form.get('ssh_command', '').split('\r\n')
    return_value = model.host_ssh_command(host_id, system_user, system_password, ssh_command)
    status_dict = {'status' : 200, 'return_value' : return_value}
    return json.dumps(status_dict)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=10000, debug=True)