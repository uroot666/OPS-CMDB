#encoding=UTF-8
import json
import gconf
import pymysql
import dbutils

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
