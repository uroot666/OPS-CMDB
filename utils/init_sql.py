#encoding=utf-8
import pymysql
from config import config

# 创建数据库
SQL_CREATE_CMDB = '''CREATE DATABASE cmdb'''

# 用户信息
SQL_CREATE_USER = '''create table cmdb.user(
    id int primary key auto_increment,
    name varchar(30),
    password varchar(40),
    email varchar(40),
    age int
)'''

# 机房
SQL_CREATE_IDC_DETAILED = '''create table cmdb.idc_detailed(
    id int primary key auto_increment,
    idcname varchar(40),
    area text,
    ip_segment varchar(50),
    machine_number int
)'''

# 资产
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

# agent信息存储
SQL_CREATE_MONITOR_HOST = '''create table cmdb.monitor_host(
    id int primary key auto_increment,
    ip varchar(128) comment '客户端IP',
    cpu float comment 'cpu使用率',
    mem float comment '内存使用率',
    disk float comment '硬盘使用率',
    m_time datetime comment '客户端发送时间',
    r_time datetime comment '服务器写入数据库时间'
)engine=innodb default charset=utf8;'''

# 告警信息存储
SQL_ALERT_CREATE = '''create table alert(
    id int primary key auto_increment,
    ip varchar(128) comment '告警客户端IP',
    message varchar(128) comment '告警内容',
    admin varchar(64) comment '资源使用人(管理员)',
    status int comment '状态，1表示未处理，0表示已处理',
    type int comment '类型，1表示显示，2表示逻辑删除',
    c_time datetime comment '告警时间',
    d_time datetime comment '逻辑删除时间'
)engine=innodb default charset=utf8;'''

# 日志分析存储
SQL_LOG_ANALYSIS = '''create table log_analysis(
    id int primary key auto_increment,
    ip varchar(128) comment '来访者IP',
    url varchar(2083) comment '被访问URL',
    code varchar(64) comment '访问状态码',
    count int comment '总次数'
)engine=innodb default charset=utf8;'''

# 
SQL_LOG = '''create table log(
    id int primary key auto_increment,
    a_time datetime comment '访问时间',
    ip varchar(128) comment '来访者IP',
    url varchar(2083) comment '被访问URL',
    code int comment '访问状态码',
    city_name varchar(64) comment '城市名字'
)engine=innodb default charset=utf8;'''

#
SQL_geoip = '''create table geoip(
    id int primary key auto_increment,
    city_name varchar(64) comment '城市名字',
    city_lat float comment '城市纬度',
    city_lgt float comment '城市经度'
)engine=innodb default charset=utf8;'''