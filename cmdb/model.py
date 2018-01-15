#encoding=UTF-8
import json
import pymysql
import datetime
import os

from . import gconf
from . import dbutils
from utils import encryption

SQL_MONITOR_HOST_CREATE = 'insert into monitor_host(ip, cpu, mem, disk, m_time, r_time) value(%s, %s, %s, %s, %s, %s)'
SQL_MONITOR_HOST_LIST = 'select ip, cpu, mem, disk, m_time from monitor_host where ip=%s and r_time >= %s order by m_time asc'

class User(object):
    KEY = 'id'
    SQL_VALIDATE_LOGIN = 'select id,name from user where name = %s and password = %s'
    SQL_VALIDATE_LOGIN_COLUMS = ("id", "name")
    SQL_USER_LIST = 'select id, name, age, email from user'
    SQL_USER_LIST_COLUMS = ("id", "username", "age", "email")
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
        cnt, record = dbutils.user_db_operating(cls.SQL_VALIDATE_LOGIN, True, (username, encryption.md5_str(password)))
        return dict(zip(cls.SQL_VALIDATE_LOGIN_COLUMS, record[0])) if record else None

    #读出用户数据，并转换成列表返回
    @classmethod
    def get_list(cls):
        cnt, users = dbutils.user_db_operating(cls.SQL_USER_LIST, True)
        return [dict(zip(cls.SQL_USER_LIST_COLUMS, user)) for user in users]

    # 根据id查询出用户信息
    @classmethod
    def get_user_by_id(cls, uid):
        cnt, record = dbutils.user_db_operating(cls.SQL_GET_USER_BY_ID, True, (uid,))
        if len(record) != 0:
            record = record[0]
        return  dict(zip(cls.SQL_GET_USER_BY_ID_COLUMS, record)) if record else {}

    # 根据id删除用户
    @classmethod
    def delete_by_key(cls, value, key=None):
        sql = cls.SQL_USER_DELETE_BY_KEY.format(key=cls.KEY if key is None else key)
        dbutils.user_db_operating(sql, False, (value,))
        return True

    @classmethod
    def get_by_key(cls, value, key=None):
        sql = cls.SQL_GET_USER_BY_KEY.format(key=cls.KEY if key is None else key)
        _, record = dbutils.user_db_operating(sql, True, (value,))
        if len(record) != 0:
            record = record[0]
        return  dict(zip(cls.SQL_GET_USER_BY_KEY_COLUMS, record)) if record else {}

    # 判断用户是否存在
    @classmethod
    def validate_user_modify(cls, id, username, age):
        return True

    def user_edit_save(self):
        dbutils.user_db_operating(self.SQL_USER_EDIT_SAVE, False, (self.username, self.age, self.email, self.id))

    # 添加用户
    def save(self):
        dbutils.user_db_operating(self.SQL_USER_CREATE, False, (self.username, encryption.md5_str(self.password), self.age, self.email))

    # 修改密码，判断旧密码是否正确
    @classmethod
    def judgment_old_password(cls, uid, old_password):
        cnt, rt_list = dbutils.user_db_operating(cls.SET_PASSWORD_SELECT, False, (uid,encryption.md5_str(old_password)))
        return cnt > 0

    # 修改密码，更新密码
    def set_password(self):
        dbutils.user_db_operating(self.SET_PASSWORD_UPDATE, False, (encryption.md5_str(self.password), self.id))

def monitor_host_create(req):
    values = []
    for key in ['ip', 'cpu', 'mem', 'disk', 'm_time']:
        values.append(req.get(key, ''))
    values.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dbutils.idc_db_operating(SQL_MONITOR_HOST_CREATE, False, tuple(values))

# 返回监控数据（cpu，disk, mem）
def monitor_host_list(ip):
    start_time = (datetime.datetime.now() - datetime.timedelta(days = 10)).strftime('%Y-%m-%d %H:%M:%S')
    rt_list = dbutils.idc_db_operating(SQL_MONITOR_HOST_LIST, True, (ip,start_time))
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
    # result = {
    #     'categories' : ['一月', '二月', '三月', '四月', '五月', '六月','七月', '八月', '九月', '十月', '十一月', '十二月'],
    #     'serial' : [{
    #         'name': 'CPU',
    #         'data': [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2,
    #             26.5, 23.3, 18.3, 13.9, 9.6]
    #         }, 
    #         {
    #         'name': '内存',
    #         'data': [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8,
    #             24.1, 20.1, 14.1, 8.6, 2.5]
    #         }, 
    #         {
    #         'name': '磁盘',
    #         'data': [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6,
    #             17.9, 14.3, 9.0, 3.9, 1.0]
    #         }]
    # }
    return result

# 查询出所有未处理的告警记录
SQL_GET_MOITOR_LOG = "select id,ip,message,admin,status,type,c_time from alert where type=1"
SQL_GET_MOITOR_LOG_COLUMS = ('id', 'ip', 'message', 'admin', 'status', 'type', 'c_time')
def get_moitor_log():
    moitor_log_list = dbutils.idc_db_operating(SQL_GET_MOITOR_LOG, True)
    log_list = []
    for moitor_log in moitor_log_list:
        moitor_log = dict(zip(SQL_GET_MOITOR_LOG_COLUMS,moitor_log))
        if moitor_log['c_time']:
            moitor_log['c_time'] = moitor_log['c_time'].strftime('%Y-%m-%d %H:%M:%S')
        log_list.append(moitor_log)
    return log_list

SQL_MONITOR_LOG_DELETE = "update alert set type=2,d_time=%s where id = %s"
def monitor_log_delete(id):
    d_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dbutils.idc_db_operating(SQL_MONITOR_LOG_DELETE, False, (d_time, id))
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
    return result_file

#分析log文件并返回倒数topn行
def gethtml(src, topn=10):
    stat_dict = {}
    fhandler = open(src, "r")
    for line in fhandler:
        line_list = line.split()
        key = (line_list[0], line_list[6], line_list[8])
        stat_dict[key] = stat_dict.setdefault(key, 0) + 1
    fhandler.close()

    results = sorted(stat_dict.items(), key=lambda x:x[1])
    results = results[: -topn - 1:-1]
    RESULT__COLUMS = ('ip', 'url', 'code','count')
    req = []
    for result in results:
        if result:
            result = [result[0][0], result[0][1], result[0][2], result[1]]
            result = dict(zip(RESULT__COLUMS, result))
        req.append(result)
    return req