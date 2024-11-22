import time
import unittest
import requests
import os
import sys
import threading
from BeautifulReport import BeautifulReport
from httpStubFramework.threadCount import check_server_start, server_lst
from client_stub import fileAppStub

DIR = os.path.dirname(os.path.abspath(__file__))
Environ = 'Online'


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = 'report.html'
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir=DIR)


# start server
def start_server():
    os.chdir(DIR + '/app')
    os.system('python docteamApp.py')  # ./XXX.sh


if __name__ == '__main__':
    # fileApp stub start
    fileAppStub.start_stub()

    # server start
    t = threading.Thread(target=start_server)
    t.start()

    # check stub start
    check_server = {'http_stub', 'socket_server'}
    check_server_start(check_server)

    # testCase Run
    testsuite = unittest.defaultTestLoader.discover(
        start_dir=DIR + '/testCase',
        pattern='test*.py'
    )
    run(testsuite)

    # stub shutdown
    fileAppStub.shutdown_stub()

    # server stop
    os.chdir(DIR + '/app')
    os.system('python appStop.py')

