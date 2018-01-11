# cmdb
## cmdb server
1. web 框架使用flask
2. 数据库使用mysql,使用pymysql连接
3. 前端框架使用bootstrap
4. requests模块

## cmdb agent
1. 使用了psutil, requests模块

## 前端使用
1. bootstrap
2. sweetalert
3. datatables
4. jQuery
5. Highcharts
6. datepicker


## 功能模块
1. 资源监控
    说明：通过Highcharts展示数据库存储的客户端发发送的数据，使用JS定时器定时刷新。
2. 监控告警(monitor_alert.py)
    说明： 检查一段时间内的资源情况，如果超过则发送邮件告警
    使用： 邮件告警的收件邮箱为资产使用者的邮箱
    