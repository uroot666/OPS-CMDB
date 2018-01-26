#encoding=utf-8
import json
import pymysql
import datetime
import os
import time
import geoip2.database

from utils import dbutils
from utils import encryption
from utils import ssh_remotely

from cmdb import app

SQL_ENGINEROOM_LIST = "select id,idcname,area,ip_segment,machine_number from idc_detailed"
SQL_ENGINEROOM_LIST_COLUMS = ('id', 'idcname', 'area','ip_segment', 'engineroom_number')
SQL_IDC_ADD_SAVE = "insert into idc_detailed(idcname, area, ip_segment, machine_number) value (%s, %s, %s, %s)"
SQL_IDC_VIEW_SAVE = "update idc_detailed set idcname=%s,area=%s,ip_segment=%s,machine_number=%s where id=%s"
SQL_IDC_TAILS_GET = "select idcname,area,ip_segment,machine_number from idc_detailed where id=%s"
SQL_IDC_TAILS_GET_COLUMS = ('idcname', 'area','ip_segment', 'engineroom_number')
SQL_IDC_DELETE = "delete from idc_detailed where id=%s"
SQL_GET_ASSET = "select id,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status from asset where status != 2"
SQL_GET_ASSET_COLUMS = ("id","sn","hostname","os","ip","machine_room_id","vendor","model","ram","cpu","disk","time_on_shelves","over_guaranteed_date","buiness","admin","status")
SQL_ASSET_DELETE = "delete from asset where id=%s"
SQL_GET_ASSET_BY_ID = "select id,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status from asset where id = %s"
SQL_GET_ASSET_BY_ID_COLUMS = ("id","sn","hostname","os","ip","machine_room_id","vendor","model","ram","cpu","disk","time_on_shelves","over_guaranteed_date","buiness","admin","status")
SQL_ASSET_SAVE = 'insert into asset(sn,hostname,os,vendor,ip,model,cpu,ram,disk,admin,buiness,machine_room_id,time_on_shelves,over_guaranteed_date,status) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
SQL_ASSET_UPDATE = 'update asset set sn=%s,hostname=%s,os=%s,ip=%s,vendor=%s,model=%s,cpu=%s,ram=%s,disk=%s,admin=%s,buiness=%s,machine_room_id=%s,time_on_shelves=%s,over_guaranteed_date=%s,status=%s where id=%s'
SQL_GET_ASSET_BY_IP = "select id,sn,hostname,os,ip,machine_room_id,vendor,model,ram,cpu,disk,time_on_shelves,over_guaranteed_date,buiness,admin,status from asset where ip = %s"
SQL_GET_ASSET_BY_IP_COLUMS = ("id","sn","hostname","os","ip","machine_room_id","vendor","model","ram","cpu","disk","time_on_shelves","over_guaranteed_date","buiness","admin","status")

SQL_MONITOR_HOST_CREATE = 'insert into monitor_host(ip, cpu, mem, disk, m_time, r_time) value(%s, %s, %s, %s, %s, %s)'
SQL_MONITOR_HOST_LIST = 'select ip, cpu, mem, disk, m_time from monitor_host where ip=%s and r_time >= %s order by m_time asc'

SQL_GET_MOITOR_LOG = "select id,ip,message,admin,status,type,c_time from alert where type=1"
SQL_GET_MOITOR_LOG_COLUMS = ('id', 'ip', 'message', 'admin', 'status', 'type', 'c_time')

# SQL_GET_LOG_ANALYSIS = 'select ip, url, code, count from log_analysis order by count desc limit %s'
SQL_GET_LOG_ANALYSIS = 'select ip, url, code, count(*) as cnt from log group by ip, url, code order by cnt desc limit %s'
SQL_GET_LOG_ANALYSIS_COLUMS = ('ip', 'url', 'code', 'count')
SQL_INSET_LOG_ANALYSIS = 'insert into log_analysis(ip, url, code, count) values(%s, %s, %s, %s)'

SQL_GET_CODE_COUNT = 'select count(*) as count, code from log group by code;'
SQL_GET_CODE_COUNT_COLUMS = ('value', 'name')

SQL_log_ip_distributed1 = 'select city_name,city_lgt,city_lat from geoip;'
SQL_log_ip_distributed2 = 'select city_name, count(*) as count from log group by city_name;'

SQL_MONITOR_LOG_DELETE = "update alert set type=2,d_time=%s where id = %s"

# 用户类
class User(object):
    KEY = 'id'
    SQL_VALIDATE_LOGIN = 'select id,name,admin from user where name = %s and password = %s'
    SQL_VALIDATE_LOGIN_COLUMS = ("id", "name", "admin")
    SQL_USER_LIST = 'select id, name, age, email from user'
    SQL_USER_LIST_COLUMS = ("uid", "username", "age", "email")
    SQL_GET_USER_BY_ID = 'select id,name,age,email from user where id = %s'
    SQL_GET_USER_BY_KEY = 'select id,name,age,email from user where {key} = %s'
    SQL_GET_USER_BY_KEY_COLUMS = ("uid", "username", "age", "email")
    SQL_GET_USER_BY_ID_COLUMS = ("uid", "username", "age", "email")
    SQL_USER_CREATE = 'insert into user(name, password, age, email) value( %s, %s, %s, %s)'
    SQL_USER_DELETE_BY_KEY = 'delete from user where {key} = %s'
    SQL_USER_EDIT_SAVE = 'update user set name = %s, age = %s, email = %s where id = %s'
    SET_PASSWORD_SELECT = "select * from user where id=%s and password=%s"
    SET_PASSWORD_UPDATE = "update user set password=%s where id = %s"


    def __init__(self, id, username, password, age, email):
        self.id = id
        self.username = username.strip()
        self.password = password.strip()
        self.age = age
        self.email = email.strip()
        
    # 查询数据库比对用户密码
    @classmethod
    def validate_login(cls, username, password):
        cnt, record = dbutils.db_operating(cls.SQL_VALIDATE_LOGIN, True, (username, encryption.md5_str(password)))
        return dict(zip(cls.SQL_VALIDATE_LOGIN_COLUMS, record[0])) if record else None

    #读出用户数据，并转换成列表返回
    @classmethod
    def get_list(cls):
        cnt, users = dbutils.db_operating(cls.SQL_USER_LIST, True)
        return [dict(zip(cls.SQL_USER_LIST_COLUMS, user)) for user in users]

    # 根据id查询出用户信息
    @classmethod
    def get_user_by_id(cls, uid):
        cnt, record = dbutils.db_operating(cls.SQL_GET_USER_BY_ID, True, (uid,))
        if len(record) != 0:
            record = record[0]
        return  dict(zip(cls.SQL_GET_USER_BY_ID_COLUMS, record)) if record else {}

    # 根据id删除用户
    @classmethod
    def delete_by_key(cls, value, key=None):
        sql = cls.SQL_USER_DELETE_BY_KEY.format(key=cls.KEY if key is None else key)
        dbutils.db_operating(sql, False, (value,))
        return True
    
    # 根据key查询用户
    @classmethod
    def get_by_key(cls, value, key=None):
        sql = cls.SQL_GET_USER_BY_KEY.format(key=cls.KEY if key is None else key)
        _, record = dbutils.db_operating(sql, True, (value,))
        if len(record) != 0:
            record = record[0]
        return  dict(zip(cls.SQL_GET_USER_BY_KEY_COLUMS, record)) if record else {}

    # 判断用户是否存在
    @classmethod
    def validate_user_modify(cls, id, username, age):
        return True

    # 保存修改的用户信息
    def user_edit_save(self):
        dbutils.db_operating(self.SQL_USER_EDIT_SAVE, False, (self.username, self.age, self.email, self.id))

    # 添加用户
    def save(self):
        dbutils.db_operating(self.SQL_USER_CREATE, False, (self.username, encryption.md5_str(self.password), self.age, self.email))

    # 修改密码，判断旧密码是否正确
    @classmethod
    def judgment_old_password(cls, uid, old_password):
        cnt, rt_list = dbutils.db_operating(cls.SET_PASSWORD_SELECT, False, (uid,encryption.md5_str(old_password)))
        return cnt > 0

    # 修改密码，更新密码
    def set_password(self):
        dbutils.db_operating(self.SET_PASSWORD_UPDATE, False, (encryption.md5_str(self.password), self.id))

# 保存客户端发回的数据
def monitor_host_create(req):
    values = []
    for key in ['ip', 'cpu', 'mem', 'disk', 'm_time']:
        values.append(req.get(key, ''))
    values.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dbutils.db_operating(SQL_MONITOR_HOST_CREATE, False, tuple(values))

# 返回监控数据（cpu，disk, mem）
def monitor_host_list(ip):
    start_time = (datetime.datetime.now() - datetime.timedelta(days = 20)).strftime('%Y-%m-%d %H:%M:%S')
    _, rt_list = dbutils.db_operating(SQL_MONITOR_HOST_LIST, True, (ip,start_time))
    categoy_list, cpu_list, disk_list, mem_list = [], [], [], []
    for line in rt_list:
        categoy_list.append(line[4].strftime('%H:%M'))
        cpu_list.append(line[1])
        disk_list.append(line[3])
        mem_list.append(line[2])

    result = {
        'categories' : categoy_list,
        'serial' : [{
                'name':'CPU',
                'data':cpu_list
            },{
                'name':'磁盘',
                'data':disk_list
            },{
                'name':'内存',
                'data':mem_list
            }]
        }
    return result

# 查询出所有未处理的告警记录
def get_moitor_log():
    _, moitor_log_list = dbutils.db_operating(SQL_GET_MOITOR_LOG, True)
    log_list = []
    for moitor_log in moitor_log_list:
        moitor_log = dict(zip(SQL_GET_MOITOR_LOG_COLUMS,moitor_log))
        if moitor_log['c_time']:
            moitor_log['c_time'] = moitor_log['c_time'].strftime('%Y-%m-%d %H:%M:%S')
        log_list.append(moitor_log)
    return log_list

# 逻辑上删除日志记录,在前端不显示
def monitor_log_delete(id):
    d_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dbutils.db_operating(SQL_MONITOR_LOG_DELETE, False, (d_time, id))
    return {'code':200}

# 判断上传文件是否符合规范
def upload_allowed_file(ALLOWED_EXTENSIONS, filname):
    if '.' in filname and filname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True

# 上传文件处理函数
def upload(file, ALLOWED, save_path): #file文件数据流，ALLOWED允许后缀，save_path保存路径
    result_file = ''
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = file.filename
    if upload_allowed_file(ALLOWED, filename):
        file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.' + filename.rsplit('.', 1)[1] #文件新名字
        result_file = os.path.join(save_path, file_name)
        file.save(result_file)
        status = log_import(result_file)
    return (result_file, status)

# 保存上传的日志部分信息，以及IP访问IP的对应的地理位置
def log_import(filname):
    SQL_LOG_SAVE = 'insert into log(a_time, ip, url, code, city_name) values(%s, %s, %s, %s, %s)'
    SQL_GEOIP_SAVE = 'insert into geoip(city_name, city_lat, city_lgt) values(%s, %s, %s)'
    log_list = []
    geoip_list = []
    fhandler = None
    geo_reader = None
    if os.path.exists(filname):
        try:
            fhandler = open(filname, "r")
            geo_reader = geoip2.database.Reader(app.config['GeoIP'])
            for line in fhandler:
                try:
                    elements = line.split()
                    a_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(elements[3], '[%d/%b/%Y:%H:%M:%S'))
                    ip = elements[0]
                    url = elements[6]
                    code = elements[8]
                    response = geo_reader.city(ip)
                    if response.country.names.get('en', '').lower() == 'china':
                        city_name = response.city.names.get('zh-CN', '')
                        if city_name:
                            city_lat = response.location.latitude
                            city_lgt = response.location.longitude
                            log_list.append((a_time, ip, url, code, city_name))
                            geoip_list.append((city_name, city_lat, city_lgt))
                except BaseException as e:
                    print(e)
            geoip_list = list(set(geoip_list))
            dbutils.list_db_insert(SQL_LOG_SAVE, False, log_list)
            dbutils.list_db_insert(SQL_GEOIP_SAVE, False, geoip_list)
        except BaseException as e:
            print(e)
            return {'status' : 'error'}
        finally:
            if geo_reader:
                geo_reader.close()
            if fhandler:
                fhandler.close()
                os.remove(filname)
        return {'status' : 'ok'}

# 根据ID查询机房信息
def idc_tails_get(id):
    _, idc_tails = dbutils.db_operating(SQL_IDC_TAILS_GET, True, (id,))
    if len(idc_tails) != 0:
        idc_tails = idc_tails[0]
    return dict(zip(SQL_IDC_TAILS_GET_COLUMS, idc_tails))

# 返回所有机房信息
def engineroom_list():
    _, rt_list = dbutils.db_operating(SQL_ENGINEROOM_LIST, True)
    return [dict(zip(SQL_ENGINEROOM_LIST_COLUMS, engineroom)) for engineroom in rt_list]

# 添加机房
def idc_add_save(idcname, area, ip_segment, machine_number):
    dbutils.db_operating(SQL_IDC_ADD_SAVE, False, (idcname, area, ip_segment, machine_number))

# 保存修改机房信息
def idc_view_save(idcid, idcname, area, ip_segment, machine_number):
    dbutils.db_operating(SQL_IDC_VIEW_SAVE, False, (idcname, area, ip_segment, machine_number, idcid))

# 根据IP删除机房
def idcroom_delete(id):
    dbutils.db_operating(SQL_IDC_DELETE, False,(id,))

# 获取所有资产信息
def get_asset():
    _, asset_list = dbutils.db_operating(SQL_GET_ASSET, True)
    assets = []
    for asset in asset_list:
        asset = dict(zip(SQL_GET_ASSET_COLUMS,asset))
        for key in ('time_on_shelves','over_guaranteed_date'):
            if asset[key]:
                asset[key] = asset[key].strftime('%Y-%m-%d')
        asset['machine_room_id'] = idc_tails_get(asset['machine_room_id'])['idcname']
        assets.append(asset)
    return assets

# 删除资产信息
def asset_delete(id):
    dbutils.db_operating(SQL_ASSET_DELETE, False, (id,))

# 根据id查询资产
def get_asset_by_id(id):
    _, assets = dbutils.db_operating(SQL_GET_ASSET_BY_ID, True, (id))
    asset = dict(zip(SQL_GET_ASSET_BY_ID_COLUMS, assets[0]))
    for key in ('time_on_shelves','over_guaranteed_date'):
        if asset[key]:
            asset[key] = asset[key].strftime('%Y-%m-%d')
    return asset

# 根据IP查询出asset
def get_asset_by_ip(ip):
    _, assets = dbutils.db_operating(SQL_GET_ASSET_BY_IP, True, (ip))
    asset = dict(zip(SQL_GET_ASSET_BY_IP_COLUMS, assets[0]))
    for key in ('time_on_shelves','over_guaranteed_date'):
        if asset[key]:
            asset[key] = asset[key].strftime('%Y-%m-%d')
    return asset

# 保存资产信息
def asset_save(asset_args):
    dbutils.db_operating(SQL_ASSET_SAVE, False, asset_args)
    return 200

# 保存资产修改信息
def asset_update(update_args):
    dbutils.db_operating(SQL_ASSET_UPDATE, False, update_args)
    return 200


# 查询访问次数的前topn的信息（log日志）
def get_log_analysis(topn):
    _, res_list = dbutils.db_operating(SQL_GET_LOG_ANALYSIS, True, (topn,))
    req = []
    for line in res_list:
        res = dict(zip(SQL_GET_LOG_ANALYSIS_COLUMS, line))
        req.append(res)
    return req


# 远程执行命令
def host_ssh_command(host_id, system_user, system_password, ssh_command):
    asset = get_asset_by_id(host_id)
    host_ip = asset.get('ip')
    port = 22
    return_value = ssh_remotely.exec_cmds(host_ip, port, system_user, system_password, ssh_command)
    return return_value

# 查询日志里面所有状态码及数量
def log_code_dist():
    log_code_dist_data_list = []
    log_code_dist_legend_list = []
    _, data = dbutils.db_operating(SQL_GET_CODE_COUNT, True)
    for line in data:
        log_code_dist_legend_list.append(line[1])
        line = dict(zip(SQL_GET_CODE_COUNT_COLUMS, line))
        log_code_dist_data_list.append(line)
    return log_code_dist_data_list,log_code_dist_legend_list

# 查询单位小时内各个状态码的数量，目前是假数据，因为不合逻辑，数据只是用来测试展示效果
def log_code_time_dist():
    sql2 = "select code, count(*) as count, date_format(a_time, '%%Y-%%m-%%d %%H:00:00') as time from log group by time, code limit 100;"
    _, rt_list = dbutils.db_operating(sql2, True)
    legend = []
    xAxis = []
    series = []
    temp_data = {}
    for line in rt_list:
        if line[0] not in legend:
            legend.append(line[0])
        if line[2] not in xAxis:
            xAxis.append(line[2])
        temp_data.setdefault(line[0], {})
        temp_data[line[0]][line[2]] = line[1]
    xAxis.sort()
    for code in legend:
        code_time_date = []
        for time in xAxis:
            code_time_date.append(temp_data[code].get(time, 0))
        series.append({'name':code, 'type':'bar', 'stack':'code', 'data':code_time_date})
    return legend,xAxis,series

# 查询log里面IP的经纬度，返回给IP分布图使用
def log_ip_distributed():
    server_ip = '14.17.88.1'
    log_ip_distributed_geoCoord = {}
    log_ip_distributed_markLine = []
    log_ip_distributed_markPoint = []
    try:
        print(app.config['GeoIP'])
        geo_reader = geoip2.database.Reader(app.config['GeoIP'])
        response = geo_reader.city(server_ip)
        server_name = response.city.names.get('zh-CN', '')
        server_lgt = response.location.longitude
        server_lat = response.location.latitude
    finally:
        geo_reader.close()
        log_ip_distributed_geoCoord[server_name] = [server_lgt, server_lat]

    _, rt_list = dbutils.db_operating(SQL_log_ip_distributed1, True)
    for line in rt_list:
        log_ip_distributed_geoCoord[line[0]] = [line[1], line[2]]
    
    _, rt_list = dbutils.db_operating(SQL_log_ip_distributed2, True)
    for line in rt_list:
        log_ip_distributed_markLine.append([{'name':line[0]}, {'name':server_name, 'value':line[1]}])
        log_ip_distributed_markPoint.append({'name':line[0], 'value':line[1]})

    return log_ip_distributed_geoCoord, log_ip_distributed_markLine, log_ip_distributed_markPoint