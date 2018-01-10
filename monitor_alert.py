#encoding: utf-8

import datetime
from utils import dbutils

INTERVAL = 100

#阀值
policies = {
    'cpu':{'count':3, 'ceil':80},
    'mem':{'count':3, 'ceil':75},
    'disk':{'count':3, 'ceil':85},
}

SELECT_MONITOR_HOST = 'select ip,cpu,mem,disk from monitor_host where r_time >= %s'
SELECT_MONITOR_HOST_COLUMNS = {1:'cpu', 2:'mem', 3:'disk'}
SQL_ALERT_CREATE = 'insert into alert(ip,message,admin,status,type,c_time) values(%s, %s, %s, 1, 1, %s)'

#查询出超过阀值的主机
def monitor_alert():
    r_time = (datetime.datetime.now() - datetime.timedelta(minutes=INTERVAL)).strftime("%Y-%m-%d %H:%M:%S")
    _, rt_list = dbutils.db_operating(SELECT_MONITOR_HOST, True, (r_time,))
    rt_dict = {}
    for line in rt_list:
        rt_dict.setdefault(line[0], {'cpu' : 0, 'mem' : 0, 'disk' : 0})
        for key, value in SELECT_MONITOR_HOST_COLUMNS.items():
            if line[key] > policies[value]['ceil']:
                rt_dict[line[0]][value] += 1

    for key in rt_dict:
        messages = []
        for resource in SELECT_MONITOR_HOST_COLUMNS.values():
            if rt_dict[key][resource] > policies[resource]['count']:
                messages.append('%s超过%s分钟内%s次超过阀值%s%%' % (resource, INTERVAL, policies[resource]['count'], policies[resource]['ceil']))
        if messages:
            c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dbutils.db_operating(SQL_ALERT_CREATE, False, (key, ','.join(messages), 'uroot', c_time))

if __name__ == '__main__':
    monitor_alert()