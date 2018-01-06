#encoding=UTF-8
import json
import gconf
import pymysql
import dbutils
import datetime
#sql template
SQL_VALIDATE_LOGIN = 'select id,name from user where name = %s and password = md5(%s)'
SQL_VALIDATE_LOGIN_COLUMS = ("id", "name")
SQL_USER_LIST = 'select id, name, age, email from user'
SQL_USER_LIST_COLUMS = ("id", "username", "age", "email")
SQL_GET_USER_BY_ID = 'select id,name,age,email from user where id = %s'
SQL_GET_USER_BY_ID_COLUMS = ("uid", "username", "age", "email")
SQL_USER_EDIT_SAVE = 'update user set name = %s, age = %s, email = %s where id = %s'
SQL_USER_DELETE = 'delete from user where id = %s'
SQL_USER_CREATE = 'insert into user(name, password, age, email) value( %s, md5(%s), %s, %s)'

SQL_MONITOR_HOST_CREATE = 'insert into monitor_host(ip, cpu, mem, disk, m_time, r_time) value(%s, %s, %s, %s, %s, %s)'
SQL_MONITOR_HOST_LIST = 'select ip, cpu, mem, disk, m_time from monitor_host where ip=%s and r_time >= %s order by m_time asc'

#读出用户数据，并转换成列表返回
def get_users():
    cnt, users = dbutils.user_db_operating(SQL_USER_LIST, True)
    return [dict(zip(SQL_USER_LIST_COLUMS, user)) for user in users]
    # db = pymysql.connect(**config.config)
    # cursor = db.cursor()
    # cursor.execute(SQL_USER_LIST)
    # users = cursor.fetchall()
    # cursor.close()
    # db.close()
    # return [dict(zip(SQL_USER_LIST_COLUMS, user)) for user in users]


    # fh = open(gconf.USER_DATA_PATH, 'r')
    # users = json.loads(fh.read())
    # print(users)
    # fh.close()
    # return users

# 查询数据库比对用户密码
def validate_login(username, password):
    cnt, record = dbutils.user_db_operating(SQL_VALIDATE_LOGIN, True, (username, password))
    if len(record) != 0:
        record = record[0]
    return dict(zip(SQL_VALIDATE_LOGIN_COLUMS, record)) if record else None

    # db = pymysql.connect(**config.config)
    # cursor = db.cursor()
    # cursor.execute(SQL_VALIDATE_LOGIN,(username, password ))
    # record = cursor.fetchone()
    # cursor.close()
    # db.close()
    # return  dict(zip(SQL_VALIDATE_LOGIN_COLUMS, record)) if record else None
    
    # 循环验证用户数据中用户及密码
    # users = get_users()
    # for user in users:
    #     if  user.get('username') == username and user.get('password') == password:
    #         return user
    # return None

def get_user_by_id(uid):
    cnt, record = dbutils.user_db_operating(SQL_GET_USER_BY_ID, True, (uid,))
    if len(record) != 0:
        record = record[0]
    return  dict(zip(SQL_GET_USER_BY_ID_COLUMS, record)) if record else {}

    # db = pymysql.connect(**config.config)
    # cursor = db.cursor()
    # cursor.execute(SQL_GET_USER_BY_ID,(uid,))
    # record = cursor.fetchone()
    # cursor.close()
    # db.close()
    # return  dict(zip(SQL_GET_USER_BY_ID_COLUMS, record)) if record else {}

#分析log文件并返回倒数topn行
def gethtml(src, topn=10):
    stat_dict = {}
    fhandler = open(src, "r")
    for line in fhandler:
        line_list = line.split()
        key = (line_list[0], line_list[6], line_list[8])
        stat_dict[key] = stat_dict.setdefault(key, 0) + 1
    fhandler.close()

    result = sorted(stat_dict.items(), key=lambda x:x[1])
    print(topn)
    return result[: -topn - 1:-1]
    print(topn)

def user_del(uid):
    dbutils.user_db_operating(SQL_USER_DELETE, False, (uid,))
    return True
    # db = pymysql.connect(**config.config)
    # cursor = db.cursor()
    # cursor.execute(SQL_USER_DELETE,(uid,))
    # db.commit()
    # cursor.close()
    # db.close()
    # return True

    # users = get_users()
    # index = 0
    # for user_dict in users:
    #     if user_dict.get('id') == id:
    #         users.pop(index)
    #         users = json.dumps(users)
    #         fh = open(gconf.USER_DATA_PATH, 'w')
    #         fh.write(users)
    #         fh.close
    #         return True, user_dict.get("username")
    #     else:
    #         index = index + 1
    # return None

def user_edit_jud(id, username, age):
    return True

def user_edit_save(id, username, email, age):
    dbutils.user_db_operating(SQL_USER_EDIT_SAVE, False, (username, age, email, id))
    return True

    # db = pymysql.connect(**config.config)
    # cursor = db.cursor()
    # cursor.execute(SQL_USER_EDIT_SAVE,(username, age, id))
    # db.commit()
    # cursor.close()
    # db.close()
    # return True

    # users = get_users()
    # index = 0
    # for user_dict in users:
    #     if user_dict.get('id') == id:
    #         users[index]["username"] = username
    #         users[index]["password"] = password
    #         fh = open(gconf.USER_DATA_PATH, 'w')
    #         users = json.dumps(users)
    #         fh.write(users)
    #         fh.close
    #         return True
    #     else:
    #         index = index + 1
    # return  None
    


#将添加的用户信息写入到json文件中
def user_create(username, password, age, email):
    dbutils.user_db_operating(SQL_USER_CREATE, False, (username, password, age, email))

    # db = pymysql.connect(**config.config)
    # cursor = db.cursor()
    # cursor.execute(SQL_USER_CREATE,(username, password, age))
    # db.commit()
    # cursor.close()
    # db.close()


    # temp_user_all = get_users()
    # add_user = {"id":temp_user_all[len(temp_user_all) - 1].get('id') + 1, "username":username, "password":password}
    # temp_user_all.append(add_user)
    # user_all = json.dumps(temp_user_all)
    # fh = open(gconf.USER_DATA_PATH, 'w')
    # fh.write(user_all)
    # fh.close

def monitor_host_create(req):
    values = []
    for key in ['ip', 'cpu', 'mem', 'disk', 'm_time']:
        values.append(req.get(key, ''))
    values.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    dbutils.idc_db_operating(SQL_MONITOR_HOST_CREATE, False, tuple(values))

# 返回监控数据（cpu，disk, mem）
def monitor_host_list(ip):
    start_time = (datetime.datetime.now() - datetime.timedelta(days = 10)).strftime('%Y-%m-%d %H:%M:%S')
    print(start_time)
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