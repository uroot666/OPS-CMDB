# encoding: utf-8
# cmdb agent

import time
from datetime import datetime

import psutil
import requests

INTERVAL = 1

URL = 'http://localhost:10000/monitor/host/create/'

# 获取网卡IP
def get_addr():
    addr = '0.0.0.0'
    nics = psutil.net_if_addrs()
    for k,v in nics.items():
        for item in v:
            if item[0] == 2 and not item[1]=='127.0.0.1':
                addr = item[1]
                break
    return addr

# 返回系统信息
def monitor():
    while True:
        usage = {}
        usage['ip'] = get_addr()
        usage['disk'] = psutil.disk_usage('/').percent
        usage['cpu'] = psutil.cpu_percent()
        usage['mem'] = psutil.virtual_memory().percent
        usage['m_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(usage)
        response = requests.post(URL, data=usage)
        if response.ok:
            print(response.json())
        else:
            print('error')
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt as e:
        print('使用Ctrl-C结束程序')
    finally:
        print('程序已结束')