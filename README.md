# cmdb
> python 3.6，windows环境下开发

## cmdb server
1. web框架使用flask
2. 数据库使用mysql,使用pymysql库连接
4. paramiko 远程执行命令,上传文件(用来发布agent)
5. geoip 定位IP地理位置

## 前端使用
1. 前端框架使用 bootstrap
2. js库 jQuery
3. 表格展示 datatables
4. 提示弹窗 sweetalert
5. 图表展示 Highcharts 
6. 时间 datepicker
7. 数据总览画图 echarts

## cmdb agent
1. 使用了psutil, requests模块

## 功能
### server
1. 用户，机房，资产管理
2. 资源监控
3. 监控告警(monitor_alert.py)
4. nginx日志分析

### agent
<p>监测资源使用情况，使用http接口定时发送到server端</p>

## 文件结构
CMDB
agent ---> agent文件
cmdb  ---> 资产管理的app及模板文件
config ---> 配置文件存放
restapi ---> 蓝图路由，agent使用
utiles  ---> 邮件发送、ssh等被调用模块

## 界面展示
![ad](https://github.com/uroot666/cmdb/blob/master/temp/images/1.png)

![ad](https://github.com/uroot666/cmdb/tree/master/temp/images/2.png)

![ad](https://github.com/uroot666/cmdb/tree/master/temp/images/3.png)