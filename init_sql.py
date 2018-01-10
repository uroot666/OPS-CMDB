#encoding=utf-8
import pymysql
from cmdb import config

#创建需要的数据库,添加测试数据
SQL_DROP_CMDB = '''DROP DATABASE cmdb'''
SQL_CREATE_CMDB = '''CREATE DATABASE cmdb'''
SQL_CREATE_USER = '''create table cmdb.user(
    id int primary key auto_increment,
    name varchar(30),
    password varchar(40),
    email varchar(40),
    age int
)'''

SQL_CREATE_IDC_DETAILED = '''create table cmdb.idc_detailed(
    id int primary key auto_increment,
    idcname varchar(40),
    area text,
    ip_segment varchar(50),
    machine_number int
)'''

SQL_CREATE_ASSET='''create table cmdb.asset (
    id int primary key auto_increment,
    sn varchar(125) not null unique key comment '资产编号',
    hostname varchar(64) comment '主机名',
    os varchar(64) comment '操作系统',
    ip varchar(128) comment 'ip地址',
    machine_room_id int comment '机房ID',
    vendor varchar(256) comment '生产厂商',
    model varchar(64) comment '型号',
    ram int comment '内存, 单位G',
    cpu int comment 'cpu核数',
    disk int comment '硬盘，单位G',
    time_on_shelves date comment '上架时间',
    over_guaranteed_date date comment '过保时间',
    buiness varchar(256) comment '业务',
    admin varchar(256) comment '使用者',
    status int comment '0 正在使用,1 维护,2 删除'
)'''

SQL_CREATE_MONITOR_HOST = '''create table cmdb.monitor_host(
    id int primary key auto_increment,
    ip varchar(128),
    cpu float,
    mem float,
    disk float,
    m_time datetime,
    r_time datetime
)engine=innodb default charset=utf8;'''

SQL_ALERT_CREATE = '''create table alert(
    id int primary key auto_increment,
    ip varchar(128),
    message varchar(128),
    admin varchar(64),
    status int,
    type int,
    c_time datetime
)engine=innodb default charset=utf8;'''

db = pymysql.connect(**config.config)
cursor = db.cursor()
cursor.execute(SQL_CREATE_USER)
cursor.execute(SQL_CREATE_IDC_DETAILED)
cursor.execute(SQL_CREATE_ASSET)
cursor.execute(SQL_CREATE_MONITOR_HOST)
db.commit()
cursor.close()
db.close()