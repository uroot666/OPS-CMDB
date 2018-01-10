#encoding=UTF-8
# 数据库函数

import pymysql
from cmdb import config

#model模块使用
def db_operating(sql, if_fach,args=()):
    try:
        rt_cnt, rt_list = 0, []
        db = pymysql.connect(**config.config)
        cursor = db.cursor()
        rt_cnt = cursor.execute(sql, args)
        if if_fach:
            rt_list = cursor.fetchall()
        else:
            db.commit()
    except BaseException as e:
        print('db connect error')
        print('db error')
        print('test')
    finally:
        cursor.close()
        db.close()
    return rt_cnt,rt_list