#encoding=utf-8

import pymysql
import config

def db_operating(sql, if_fach=False, args=()):
    db = pymysql.connect(**config.config)
    cursor = db.cursor()
    cursor.execute(sql, args)
    rt_list = []
    if if_fach:
        rt_list = cursor.fetchall()
    else:
        db.commit()
    cursor.close()
    db.close()
    return rt_list
    
