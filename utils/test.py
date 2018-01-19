#encoding: utf-8

import time
import logging

import threading

logger = logging.getLogger(__name__)

def cpu():
    logger.info('cup start')
    while True:
        logger.info('cpu value')
        time.sleep(10)

def mem():
    logger.info('mem start')
    while True:
        logger.info('mem value')
        time.sleep(20)

def disk():
    logger.info('disk start')
    while True:
        logger.info('disk value')
        time.sleep(30)
        break

def sleep_func(n):
    logger.info('start function:%s', n)
    time.sleep(n)
    logger.info('end function: %s', n)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_time = time.time()
    # for i in range(5):
    #     n = 10 - i
    #     sleep_func(n)
    # ent_time = time.time()
    # ths = []
    # for i in range(5):
    #     n = 10 - i
    #     th = threading.Thread(target=sleep_func, args=(n,))
    #     ths.append(th)
    #     th.start()
    # for th in ths:
    #     th.join()
    ths = {}
    th = threading.Thread(target=cpu)
    th.setDaemon(True)
    th.start()
    ths['cpu'] = th
    th = threading.Thread(target=mem)
    th.setDaemon(True)
    th.start()
    ths['mem'] = th
    th = threading.Thread(target=disk)
    th.setDaemon(True)
    th.start()
    ths['disk'] = th
    while True:
        for th in ths:
            print(th, ths[th].isAlive())
        time.sleep(10)

    ent_time = time.time()
    print('all time:',start_time - ent_time)