#encoding=utf-8
# 资产管理的所有数据库操作

import dbutils

# sql语句
SQL_ENGINEROOM_LIST = "select id,idcname,area,ip_segment,machine_number from idc_detailed"
SQL_ENGINEROOM_LIST_COLUMS = ('id', 'idcname', 'area','ip_segment', 'engineroom_number')
SQL_IDC_ADD_SAVE = "insert into idc_detailed(idcname, arexa, ip_segment, machine_number) value (%s, %s, %s, %s)"
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


def idc_tails_get(id):
    idc_tails = dbutils.idc_db_operating(SQL_IDC_TAILS_GET, True, (id,))
    if len(idc_tails) != 0:
        idc_tails = idc_tails[0]
    return dict(zip(SQL_IDC_TAILS_GET_COLUMS, idc_tails))

def engineroom_list():
    rt_list = dbutils.idc_db_operating(SQL_ENGINEROOM_LIST, True)
    print(rt_list)
    return [dict(zip(SQL_ENGINEROOM_LIST_COLUMS, engineroom)) for engineroom in rt_list]

def idc_add_save(idcname, area, ip_segment, machine_number):
    dbutils.idc_db_operating(SQL_IDC_ADD_SAVE, False, (idcname, area, ip_segment, machine_number))

def idc_view_save(idcid, idcname, area, ip_segment, machine_number):
    dbutils.idc_db_operating(SQL_IDC_VIEW_SAVE, False, (idcname, area, ip_segment, machine_number, idcid))

def idcroom_delete(id):
    dbutils.idc_db_operating(SQL_IDC_DELETE, False,(id,))

def get_asset():
    asset_list = dbutils.idc_db_operating(SQL_GET_ASSET, True)
    assets = []
    for asset in asset_list:
        asset = dict(zip(SQL_GET_ASSET_COLUMS,asset))
        for key in ('time_on_shelves','over_guaranteed_date'):
            if asset[key]:
                asset[key] = asset[key].strftime('%Y-%m-%d')
        assets.append(asset)
    return assets

def asset_delete(id):
    dbutils.idc_db_operating(SQL_ASSET_DELETE, False, (id,))

def get_asset_by_id(id):
    assets = dbutils.idc_db_operating(SQL_GET_ASSET_BY_ID, True, (id))
    asset = dict(zip(SQL_GET_ASSET_BY_ID_COLUMS, assets[0]))
    for key in ('time_on_shelves','over_guaranteed_date'):
        if asset[key]:
            asset[key] = asset[key].strftime('%Y-%m-%d')
    return asset

def asset_save(asset_args):
    dbutils.idc_db_operating(SQL_ASSET_SAVE, False, asset_args)
    return 200

def asset_update(update_args):
    dbutils.idc_db_operating(SQL_ASSET_UPDATE, False, update_args)
    return 200