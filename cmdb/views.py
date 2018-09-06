#encoding=utf-8

# from flask import Flask
import time
from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from io import StringIO
import csv

import datetime
import os
import json
import re

from cmdb import app
from cmdb import model

from utils import decorator
# app = Flask(__name__)
# app.secret_key = "\xc5T|\xc9\x1b6\x8c\xef(\xc6\xfd\x86S\x82b\x19)\xcdg\x1c3Mf\x93z|Bk"
#首页
@app.route('/')
def index():
    if session.get('user'):
        return render_template('/dashboard.html')
    return render_template('login.html')

# 登录并跳转
@app.route('/login/', methods=["POST"])
def login():
    if session.get('user'):
        return render_template('/dashboard.html')
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    user = model.User.validate_login(username, password)
    flash('登陆成功!', "success")
    if user:
        session['user'] = user
        return render_template('/dashboard.html')
    else:
        return render_template('login.html', username=username,  error='用户或密码错误')

# 显示所有用户信息
@app.route('/users/')
@decorator.login_required
def users():
    return render_template("users.html")

# 返回所有用户信息
@app.route('/users/list/')
@decorator.login_required
def user_list():
    user_all = model.User.get_list()
    return json.dumps({'data':user_all})

# 保存添加用户
@app.route('/user/create/', methods=["POST"])
@decorator.login_required
def user_create():
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
@app.route('/user/delete/', methods=['POST'])
@decorator.login_required
def userdel():
    id = int(request.form.get('id', ''))
    jud = model.User.delete_by_key(id, 'id')
    return json.dumps({'code':200})

# 返回需要修改的用户信息
@app.route('/user/view/', methods=['POST'])
@decorator.login_required
def user_view():
    user = model.User.get_user_by_id(request.form.get('uid', 0))
    return json.dumps(user)

# 保存修改的用户信息
@app.route('/user/view_save/', methods=["POST"])
@decorator.login_required
def user_view_save():
    uid = int(request.form.get('uid'))
    username = request.form.get('username')
    age = request.form.get('age')
    email = request.form.get('email')
    user = model.User(uid, username, '', age, email)
    ok = model.User.validate_user_modify(uid, username, age)
    if ok:
        user.user_edit_save()
        return json.dumps({'code':200})
    else:
        return json.dumps({'code':400})

# 修改用户密码
@app.route('/user/set/password/', methods=['POST'])
@decorator.login_required
def user_set_password_view():
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
@decorator.login_required
def upload():
    ALLOWED = set(['log', 'py']) # 允许后缀
    upload_dir = os.path.join(app.config['basedir'], 'temp')  #存储路径
    file = request.files['upload']  # 上传文件数据
    if file:
        result = model.upload(file, ALLOWED, upload_dir)
    return redirect('/log/')

#查询分析日志的结果表单页面
@app.route('/log/')
@decorator.login_required
def log_index():
    # top = request.form
    topn = request.args.get('topn', '')
    return render_template('log.html', topn = topn)

# 返回分析日志的信息给页面
@app.route('/log/list/')
@decorator.login_required
def log():
    topn = request.args.get('topn', 10)
    topn = int(topn) if str(topn).isdigit() else 10
    result = model.get_log_analysis(topn)
    # result = model.gethtml('access.log', topn)
    return json.dumps({"data" : result})

# 下载日志topn，保存为csv文件
@decorator.login_required
@app.route('/download/')
def download():
    topn = request.args.get('topn', '')
    topn = int(topn) if str(topn).isdigit() else 10
    result = model.get_log_analysis(topn)
    io = StringIO()
    csv_writer = csv.writer(io)
    csv_writer.writerow(['IP', 'URL', 'CODE', 'COUNT'])
    for line in result:
        line = [line.get('ip'), line.get('url'), line.get('code'), line.get('count')]
        csv_writer.writerow(line)
    text = io.getvalue()
    io.close()
    return text, 200, {'Content-Type':'text/csv; charset=utf-8', 'Content-disposition' : 'attachment; filename=TOP_%s_log.csv' % topn}


# 退出登录
@app.route('/logout/')
def logout():
    session.clear()
    flash('登出成功！', 'success')
    return redirect('/')

# 返回静态资源的默认页面
@app.route("/static/")
def test():
    return render_template('login.html')

# 返回资产管理页面
@app.route("/asset/")
@decorator.login_required
def asset_index():
    # 查询出所有机房的列表，返回到资产管理页面
    engineroom_all = model.engineroom_list()
    return render_template('asset.html', engineroom_all=engineroom_all)

# 返回资产信息
@app.route("/asset/list/")
@decorator.login_required
def asset_list():
    assets = model.get_asset()
    return json.dumps({"data": assets})

# 保存添加资产信息
@app.route("/asset/save/", methods=["POST"])
@decorator.login_required
def asset_save():
    as_list = []
    for key in request.form:
        as_list.append(request.form.get(key))
    asset_save_value = model.asset_save(tuple(as_list[1:]))
    return json.dumps({"code" : 200})

# 返回需要修改资产
@app.route("/asset/view/")
@decorator.login_required
def asset_view():
    aid = request.args.get('id', 0)
    view_asset_value = model.get_asset_by_id(int(aid))
    return json.dumps(view_asset_value)

# 保存修改后的资产信息
@app.route("/asset/update/", methods=["POST"])
@decorator.login_required
def asset_update():
    au_list = []
    for key in request.form:
        au_list.append(request.form.get(key))
    au_list = au_list[1:] + [au_list[0]]
    asset_update_value = model.asset_update(tuple(au_list))
    return json.dumps({"code" : 200})

# 删除资产
@app.route("/asset/delete/", methods=["POST"])
@decorator.login_required
def asset_delete():
    aid = request.form.get("id")
    if aid:
        model.asset_delete(int(aid))
        return json.dumps({"code" : 200})

# 机房页面
@app.route("/idc/")
@decorator.login_required
def idc():
    return render_template('idc_list.html')

# 机房信息页面
@app.route("/idc/list/", methods=['POST', 'GET'])
@decorator.login_required
def idc_list():
    engineroom_all = model.engineroom_list()
    return json.dumps({'data':engineroom_all})

# 返回机房添加页面
@app.route("/idc/add/")
@decorator.login_required
def idc_add():
    return render_template('idc_create.html')

# 保存添加的机房
@app.route("/idc/add_save/", methods=["POST"])
@decorator.login_required
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
@app.route("/idc/view/", methods=['POST'])
@decorator.login_required
def idc_view():
    idcid = int(request.form.get('id'))
    idc_tails = model.idc_tails_get(idcid)
    idcname = idc_tails.get("idcname")
    area = idc_tails.get("area")
    ip_segment = idc_tails.get("ip_segment")
    machine_number = idc_tails.get("engineroom_number")
    rt_dict = {"idcid":idcid, "idcname":idcname, "ip_segment":ip_segment, "area":area, "machine_number":machine_number}
    return json.dumps(rt_dict)

# 将机房修改信息保存到数据库
@app.route("/idc/view_save/", methods=['POST'])
@decorator.login_required
def idc_view_save():
    idcid = int(request.form.get('idcid'))
    idcname = request.form.get('idcname')
    area = request.form.get('area')
    ip_segment = request.form.get("ip_segment")
    machine_number = int(request.form.get('machine_number'))
    model.idc_view_save(idcid, idcname, area, ip_segment, machine_number)
    return json.dumps({'code':200})

#删除机房
@app.route("/idc/delete/", methods=['POST'])
@decorator.login_required
def idc_delete():
    id = request.form.get('id', '0')
    if re.match(r'\d+', id):
        model.idcroom_delete(int(id))
        return json.dumps({'code':200})
    else:
        return json.dumps({'code':400})

# 将agent发回的数据存储到数据库
@app.route('/monitor/host/create/', methods=['POST'])
#@decorator.login_required
def monitor_host_create():
    req = request.form
    print(req)
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
@decorator.login_required
def monitor_host_list():
    id = request.args.get('id')
    asset = model.get_asset_by_id(id)
    ip = asset.get('ip', '')
    result = model.monitor_host_list(ip)
    return json.dumps({'code':200, 'result':result})

# 返回告警日志页面
@app.route('/moitor/log/')
@decorator.guest_login_required
def moitor_log_index():
    if session.get('user') is None:
        return redirect('/')
    return render_template('moitor_log.html')

# 查询出告警日志，然会给告警页面
@app.route('/moitor/log/list/')
@decorator.guest_login_required
def moitor_log_list():
    moitor_log = model.get_moitor_log()
    return json.dumps({"data" : moitor_log})

# 删除告警日志
@app.route('/moitor/log/delete/', methods = ['POST'])
@decorator.guest_login_required
def monitor_log_delete():
    id = request.form.get('id', '')
    req = model.monitor_log_delete(id)
    return json.dumps(req)

@app.route('/host/ssh/', methods=['POST'])
@decorator.login_required
def host_ssh():
    host_id = int(request.form.get('id', ''))
    system_user = request.form.get('system_user', '')
    system_password = request.form.get('system_password', '')
    ssh_command = request.form.get('ssh_command', '').split('\r\n')
    return_value = model.host_ssh_command(host_id, system_user, system_password, ssh_command)
    status_dict = {'status' : 200, 'return_value' : return_value}
    return json.dumps(status_dict)

@app.route('/dashboard/')
@decorator.guest_login_required
def overview():
    return render_template('/dashboard.html')

@app.route('/dashboard/data/')
@decorator.guest_login_required
def dashboard():
    log_code_dist_data, log_code_dist_legend = model.log_code_dist()
    log_code_column_legend,log_code_column_xAxis,log_code_column_series = model.log_code_time_dist()
    log_ip_distributed_geoCoord, log_ip_distributed_markLine, log_ip_distributed_markPoint = model.log_ip_distributed()
    return json.dumps({'code' : 200, 
                        'data' : {
                        'log_code_dist_legend' : log_code_dist_legend,
                        'log_code_dist_data' : log_code_dist_data,
                        'log_code_column_legend' : log_code_column_legend,
                        'log_code_column_xAxis': log_code_column_xAxis,
                        'log_code_column_series': log_code_column_series,
                        'log_ip_distributed_geoCoord' : log_ip_distributed_geoCoord,
                        'log_ip_distributed_markLine' : log_ip_distributed_markLine,
                        'log_ip_distributed_markPoint' : log_ip_distributed_markPoint
                    }})

@app.route('/script/')
@decorator.guest_login_required
def script_index():
    return render_template('/externall_service.html')

@app.route('/script/whitelist/update', methods=['POST'])
@decorator.guest_login_required
def ip_whitelist_update():
    print(request.form.get('ip_whitelist').split(','))
    return json.dumps({'code': 200})

# 返回404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=10000, debug=True)