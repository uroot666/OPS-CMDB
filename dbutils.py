#encoding=UTF-8

import pymysql
import config

def db_operating(sql, if_fach,args=()):
    rt_cnt, rt_list = 0, []
    db = pymysql.connect(**config.config)
    cursor = db.cursor()
    rt_cnt = cursor.execute(sql, args)
    if if_fach:
        rt_list = cursor.fetchall()
    else:
        db.commit()
    cursor.close()
    db.close()
    return rt_cnt,rt_list