#encoding=UTF-8
# 数据库函数

import pymysql
from config import config
import traceback

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
        print('db error')
        print(traceback.format_exc())
        db.rollback()
    finally:
        cursor.close()
        db.close()
    return rt_cnt,rt_list

# 批量写入数据
def list_db_insert(sql, if_fach,args=()):
    try:
        rt_cnt, rt_list = 0, []
        db = pymysql.connect(**config.config)
        cursor = db.cursor()
        cursor.executemany(sql, args)
        if if_fach:
            rt_list = cursor.fetchall()
        else:
            db.commit()
    except BaseException as e:
        print('db error')
        print(traceback.format_exc())
        db.rollback()
    finally:
        cursor.close()
        db.close()
    return rt_list

#用户 model模块使用
# def user_db_operating(sql, if_fach,args=()):
#     try:
#         rt_cnt, rt_list = 0, []
#         db = pymysql.connect(**config.config)
#         cursor = db.cursor()
#         rt_cnt = cursor.execute(sql, args)
#         if if_fach:
#             rt_list = cursor.fetchall()
#         else:
#             db.commit()
#     except BaseException as e:
#         print('db connect error')
#         print(traceback.format_exc())
#     finally:
#         cursor.close()
#         db.close()
#     return rt_cnt,rt_list

# idc model模块使用
# def idc_db_operating(sql, if_fach=False, args=()):
#     try:
#         db = pymysql.connect(**config.config)
#         cursor = db.cursor()
#         cursor.execute(sql, args)
#         rt_list = []
#         if if_fach:
#             rt_list = cursor.fetchall()
#         else:
#             db.commit()
#     finally:
#         cursor.close()
#         db.close()
#     return rt_list