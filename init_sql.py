#encoding=utf-8
import pymysql
import config

#创建需要的数据库,添加测试数据

SQL_CREATE_USER = '''create table user(
    id int primary key auto_increment,
    name varchar(30),
    password varchar(40),
    age int
)'''

SQL_CREATE_IDC_DETAILED = '''create table idc_detailed(
    id int primary key auto_increment,
    idcname varchar(40),
    area text,
    ip_segment varchar(50),
    machine_number int
)'''

db = pymysql.connect(**config.config)
cursor = db.cursor()
cursor.execute(SQL_CREATE_USER)
cursor.execute(SQL_CREATE_IDC_DETAILED)
db.commit()
cursor.close()
db.close()