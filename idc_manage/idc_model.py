#encoding=utf-8

import idc_dbutils

SQL_ENGINEROOM_LIST = "select id,idcname,area,ip_segment,machine_number from idc_detailed"
SQL_ENGINEROOM_LIST_COLUMS = ('id', 'idcname', 'area','ip_segment', 'engineroom_number')
SQL_IDC_ADD_SAVE = "insert into idc_detailed(idcname, area, ip_segment, machine_number) value (%s, %s, %s, %s)"
SQL_IDC_VIEW_SAVE = "update idc_detailed set idcname=%s,area=%s,ip_segment=%s,machine_number=%s where id=%s"
SQL_IDC_TAILS_GET = "select idcname,area,ip_segment,machine_number from idc_detailed where id=%s"
SQL_IDC_TAILS_GET_COLUMS = ('idcname', 'area','ip_segment', 'engineroom_number')

def idc_tails_get(id):
    idc_tails = idc_dbutils.db_operating(SQL_IDC_TAILS_GET, True, (id,))
    if len(idc_tails) != 0:
        idc_tails = idc_tails[0]
    return dict(zip(SQL_IDC_TAILS_GET_COLUMS, idc_tails))

def engineroom_list():
    rt_list = idc_dbutils.db_operating(SQL_ENGINEROOM_LIST, True)
    print(rt_list)
    return [dict(zip(SQL_ENGINEROOM_LIST_COLUMS, engineroom)) for engineroom in rt_list]

def idc_add_save(idcname, area, ip_segment, machine_number):
    idc_dbutils.db_operating(SQL_IDC_ADD_SAVE, False, (idcname, area, ip_segment, machine_number))

def idc_view_save(idcid, idcname, area, ip_segment, machine_number):
    idc_dbutils.db_operating(SQL_IDC_VIEW_SAVE, False, (idcname, area, ip_segment, machine_number, idcid))
