#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
'''
@Time    : 2019/2/23 0023 14:06
@Author  : Van Huang
@Email   : huangvan0808@gmail.com
@File    : config.py
@details : The description of the contents of the file

'''
import os
import logging
import time

# 日志管理
level_name = logging.DEBUG
FORMAT = "%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s"
logging.basicConfig(level=level_name, format=FORMAT)
log_name = './log/' + 'mockserver' + '_' + 'log' + '_' + time.strftime("%Y-%m-%d", time.localtime()) + '.log'

# mock服务配置
wiremock_version = '2.21.0'
wiremock_name = 'wiremock-standalone-' + wiremock_version + '.jar'
wiremock_path = os.path.abspath(os.path.dirname(__file__))
wiremock_port = '9090'
base_url = "http://test-api.intra.casstime.com"
# base_url = "http://www.w3school.com.cn/"
host_url = 'http://127.0.0.1'
cmd = 'java ' + '-jar ' + wiremock_name + ' --port ' + wiremock_port + ' --verbose'
logging.debug(wiremock_path)
logging.debug(cmd)

# 用例管理
case_no = {'QDD': 0, 'SOS': 0, 'MS': 0, 'OMG': 0, 'VIP': 0, 'BK&X': 0, 'terminal': 0}
server_name = 'QDD'
case_name = ''
