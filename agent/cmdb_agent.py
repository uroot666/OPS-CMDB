# encoding: utf-8
# cmdb agent

import time
from datetime import datetime

import sys
import os
import signal
import logging

import psutil
import requests

loger = logging.getLogger(__name__)

INTERVAL = 3

URL = 'http://%s:%s/monitor/host/create/'

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
def monitor(server_ip, server_port):
    while True:
        try:
            usage = {}
            usage['ip'] = get_addr()
            usage['disk'] = psutil.disk_usage('/').percent
            usage['cpu'] = psutil.cpu_percent()
            usage['mem'] = psutil.virtual_memory().percent
            usage['m_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            url = URL % (server_ip, server_port)
            loger.debug(usage)
            response = requests.post(url, data=usage)
            if response.ok:
                loger.info(response.json())
            else:
                loger.error('server error')
        except BaseException as e:
            print(e)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print('usage: python cmdb_agent.py server_ip server_port')

        # 判断是否已有agent进程存在，存在则发送中断信号
        if os.path.exists('agent_pid'):
            with open('agent_pid', 'r') as fh:
                pid = int(fh.read())
                if psutil.pid_exists(pid):
                    os.kill(pid, signal.SIGINT)

        logging.basicConfig(level=logging.INFO, filename='agent.log')

        pid = os.getpid()
        loger.info('PID: %s', pid)
        with open('agent_pid', 'w') as fh:
            fh.write(str(pid))

        monitor(sys.argv[1], sys.argv[2])

    except KeyboardInterrupt as e:
        print('使用Ctrl-C结束程序')
    finally:
        print('程序已结束')