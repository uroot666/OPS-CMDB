#encoding=UTF-8

import pymysql
import config

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
<<<<<<< HEAD
        print('db connect error')
=======
        print('db error')
        print('test')
>>>>>>> 2208b3c3cfd5dd3f5377b2304117f50f3a39aa25
    finally:
        cursor.close()
        db.close()
    return rt_cnt,rt_list
