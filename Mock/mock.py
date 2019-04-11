#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.0'
'''
@Time    : 2019/2/19 0019 23:42
@Author  : Van Huang
@Email   : huangvan0808@gmail.com
@File    : mock.py
@details : mock服务管理，包含启动、停止、录制和执行

'''
import atexit
import shlex
import codecs
from subprocess import Popen, PIPE, STDOUT
import json
import requests
from string import Template
from config import *

logging.basicConfig(level=level_name, format=FORMAT)


# 异常信息捕获
class MockServerException(Exception):
    pass


class MockServerAlreadyStartedError(MockServerException):
    pass


class MockServerNotStartedError(MockServerException):
    pass


class MockServerAlreadyStartingError(MockServerException):
    pass


class MockServerRecordStartingError(MockServerException):
    pass


class MockServerRecordStoppedError(MockServerException):
    pass


path_parent = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# mock服务管理
class MockServerManage(object):
    def __init__(self, run_cmd):
        self.cmd = shlex.split(run_cmd)
        # self.cmd = run_cmd
        self.__subprocess = None
        self.__running = False

    def __enter__(self):
        logging.debug('into enter...')
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    @property
    def is_running(self):
        return self.__running

    def start(self):
        logging.info('into start...')
        logging.info(self.__running)
        logging.info(self.__subprocess)
        if self.is_running:
            # mock服务已经在该端口启动
            raise MockServerAlreadyStartedError(
                'MockServer already started on port {}'.format(wiremock_port)
            )

        try:
            logging.info(' '.join(self.cmd))
            self.__subprocess = Popen(self.cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            if not os.path.exists('./log'):
                os.makedirs('./log')
            filename = log_name
            logging.debug(filename)
            with open(filename, 'ab+') as log:
                # out_info = self.__subprocess.stdout.readlines()
                out_info = self.__subprocess.communicate()
                for line in out_info:
                    print(line)
                    log.write(line)
                #     if not Popen.poll(self.__subprocess) is None:
                #         if line == '':
                #             break
                # self.__subprocess.stdout.close()

        except OSError as e:
            # JAVA 调用失败
            raise MockServerNotStartedError(str(e))

        time.sleep(0.1)
        if self.__subprocess.poll() is not None:
            # mock服务启动失败，返回失败码
            raise MockServerNotStartedError("\n".join([
                "returncode: {}".format(self.__subprocess.returncode),
                "stdout:",
                self.__subprocess.stdout.read()
            ]))
        # 停止mock服务，清理资源
        atexit.register(self.stop, raise_on_error=False)
        self.__running = True

    def stop(self, raise_on_error=True):
        try:
            self.__subprocess.kill()
        except AttributeError:
            if raise_on_error:
                # mock服务未启动
                raise MockServerNotStartedError()


def run_mock_server():
    print('Start Mock Server...')
    run_mock = MockServerManage(cmd)
    run_mock.start()


def stop_mock_server():
    mock_host_url = wiremock_url + ':' + wiremock_port
    logging.debug('stop_mock_server: %s' % mock_host_url)
    print('Stop Mock Server...')
    try:
        requests.get(url=mock_host_url + '/__admin/recordings/status')
    except (ConnectionRefusedError, requests.exceptions.ConnectionError):
        raise MockServerNotStartedError(
            'MockServer do not started on port {}'.format(wiremock_port)
        )
    else:
        stop_response = requests.post(url=mock_host_url + '/shutdown')
        assert stop_response.status_code == 200
    print('Stop Mock ok!')


# 录制管理
class MockRecordManage(object):
    def __init__(self, record_url, mock_url, mock_port):
        self.record_url = record_url
        self.mock_url = mock_url
        self.mock_port = mock_port
        self.mock_host_url = self.mock_url + ':' + self.mock_port
        self.headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Cache-Control': 'max-age=0', 'Connection': 'keep-alive',  'Upgrade-Insecure-Requests': '1',
                        'cookies': 'csrftoken=ZClB2xmIJUZsO8bx8syOSlR0jTPATxlAca717DEcENv0zkBDjxongdniEODxykHq; _' \
                                  'ga=GA1.1.935221262.1550566816; Hm_lvt_3eec0b7da6548cf07db3bc477ea905ee=1550566816; ' \
                                  'session=.eJwlj0uKAkEQBe9SaxeV9enM9DJNflEEhW5dDXN3C9w-CF7EX9nziPNWru_jE5ey371cCzJICCgPIY4BSL0zUBOTKhlaDdXJRMeE6kM0iDbhyo4tUUCkAqaJp-W0jbRGz6lik5NSkbJJAwxrC66RAztbn31Dnd7Iy6XYeeT-fj3iuXyGqrqbkHrn9cp9pjbHuhy7SHpdqxEt7nPG8YuA8v8F0qVCMQ.XHiZIA.SkhsQOd361P_oRA94Efmt6DGdMQ',
                        }
        self.is_starting = False
        self.http_session = requests.session()
        self.mock_case_name = ''
        self.mock_server_name = ''

    def start_record(self):
        logging.debug(self.mock_host_url)
        if self.is_starting:
            # 录制服务已经启动
            raise MockServerRecordStartingError(
                'Mock record status is  starting!'
            )
        else:
            # 查看服务状态
            try:
                response = self.http_session.get(url=self.mock_host_url + '/__admin/recordings/status')
            except (ConnectionRefusedError, requests.exceptions.ConnectionError):
                raise MockServerNotStartedError(
                    'MockServer do not started on port {}'.format(wiremock_port)
                )
            else:
                response_json = json.loads(response.text)
                if response_json["status"] == "Recording":
                    # 录制服务已经启动
                    raise MockServerRecordStartingError(
                        'Mock record already started!'
                    )
                else:
                    self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                    self.http_session.headers.update(self.headers)
                    # 启动录制请求
                    record_data = {"targetBaseUrl": self.record_url, "filters": {"urlPathPattern": QDD_URL, "allowNonProxied": True}}
                    start_response = self.http_session.post(url=self.mock_host_url + '/__admin/recordings/start', data=json.dumps(record_data))
                    if start_response.status_code == 200:
                        # 再次查看服务状态
                        response = self.http_session.get(url=self.mock_host_url + '/__admin/recordings/status')
                        response_json = json.loads(response.text)
                        if response_json["status"] == "Recording":
                            self.is_starting = True
                            print('Recording...')
                        else:
                            # 录制服务启动失败
                            raise MockServerRecordStartingError(
                                'Mock record start error!'
                            )
                    else:
                        # 录制服务启动失败
                        raise MockServerRecordStartingError(
                            'Mock record start error, status_code: {}!'.format(start_response.status_code)
                        )

    def create_file(self, name, server_name):
        filename = name
        self.mock_server_name = server_name
        if not os.path.exists(path_parent + '/Case/FunctionTest/' + self.mock_server_name):
            os.makedirs(path_parent + '/Case/FunctionTest/' + self.mock_server_name)
        elif filename == '':
            case_no[self.mock_server_name] += len(os.listdir(path_parent + '/Case/FunctionTest/' + self.mock_server_name + '/'))
            filename = 'TC_' + self.mock_server_name + '_' + str(case_no[self.mock_server_name]) + '.py'
        file = path_parent + '/Case/FunctionTest/' + self.mock_server_name + '/' + filename + '.py'
        logging.debug(file)
        self.mock_case_name = file

    def change_file(self, name, old_name, server_name):
        filename_new = name
        filename_old = old_name
        self.mock_server_name = server_name
        if not os.path.exists(path_parent + '/Case/FunctionTest/' + self.mock_server_name):
            os.makedirs(path_parent + '/Case/FunctionTest/' + self.mock_server_name)
        elif filename_new == '':
            case_no[self.mock_server_name] += len(os.listdir(path_parent + '/Case/FunctionTest/' + self.mock_server_name + '/'))
            filename_new = 'TC_' + self.mock_server_name + '_' + str(case_no[self.mock_server_name]) + '.py'
            file_new = path_parent + '/Case/FunctionTest/' + self.mock_server_name + '/' + filename_new
            file = file_new
        else:
            file_new = path_parent + '/Case/FunctionTest/' + self.mock_server_name + '/' + filename_new + '.py'
            file_old = path_parent + '/Case/FunctionTest/' + self.mock_server_name + '/' + filename_old + '.py'
            if os.path.exists(file_old):
                os.rename(file_old, file_new)
            file = file_new
        logging.debug(file)
        self.mock_case_name = file

    def delete_file(self, name, server_name):
        filename = name
        file = path_parent + '/Case/FunctionTest/' + server_name + '/' + filename + '.py'
        if not os.path.exists(path_parent + '/Case/FunctionTest/' + server_name):
            print('%s目录不存在' % server_name)
        elif os.path.exists(file):
            os.remove(file)
        else:
            print('该文件不存在')

    def create_case(self, stop_response_json):
        with codecs.open(self.mock_case_name, 'w+', encoding='utf-8') as f:
            lines = []
            map_data = []
            # 设置生成mapping模板
            # 缩进8个空格，python不能空格tab混用
            space_eight = '        '
            tmp_line = Template(space_eight + "body = ${BODY}\n" + space_eight +
                           "response = requests.post(cls.url_path + '/__admin/mappings', headers=headers, data=json.dumps(body))\n" + space_eight +
                           "assert response.status_code == 201\n")
            # 读取用例模板
            template_file = codecs.open(path_parent + '/Mock/' +'runcase.template', 'r', encoding='utf-8')
            tmp_file = Template(template_file.read())
            # 替换mapping模板内容
            for i in range(len(stop_response_json['mappings'])):
            #     if 'persistent' in stop_response_json['mappings'][i].keys():
            #         stop_response_json['mappings'][i]['persistent'] = str(stop_response_json['mappings'][i]['persistent'])
                map_data.append(tmp_line.substitute(BODY=stop_response_json['mappings'][i]))
            print(map_data)
            # 替换用例模板内容
            lines.append(tmp_file.substitute(
                CLASSNAME=self.mock_server_name + 'Test',
                PATH='\'' + self.mock_host_url + '\'',
                MAP='\n'.join(map_data)))
            # 根据模板写入用例文件
            f.writelines(lines)
            template_file.close()

    def update_case(self, sql_script):
        with codecs.open(self.mock_case_name, 'w+', encoding='utf-8') as f:
            f.write(sql_script)

    def stop_record(self):
        if not self.is_starting:
            # 录制服务已经停止
            raise MockServerRecordStoppedError(
                'Mock record status is stopped!'
            )
        else:
            # 查看服务状态
            try:
                response = self.http_session.get(url=self.mock_host_url + '/__admin/recordings/status')
            except (ConnectionRefusedError, requests.exceptions.ConnectionError):
                raise MockServerNotStartedError(
                    'MockServer do not started on port {}'.format(wiremock_port)
                )
            else:
                response_json = json.loads(response.text)
                if response_json["status"] != "Recording":
                    # 录制服务已经停止
                    raise MockServerRecordStoppedError(
                        'Mock record has stopped!'
                    )
                else:
                    # 停止录制请求
                    stop_response = self.http_session.post(url=self.mock_host_url + '/__admin/recordings/stop')
                    stop_response_json = json.loads(stop_response.text)
                    logging.debug(stop_response_json)
                    if len(stop_response_json['mappings']):
                        self.create_case(stop_response_json)
                    else:
                        print('recorded no data!')
                    if stop_response.status_code == 200:
                        # 再次查看服务状态
                        response = self.http_session.get(url=self.mock_host_url + '/__admin/recordings/status')
                        response_json = json.loads(response.text)
                        if response_json["status"] == "Stopped":
                            self.is_starting = False
                            print('Stopped Record!.')
                        else:
                            # 录制服务停止失败
                            raise MockServerRecordStoppedError(
                                'Mock record start error!'
                            )
                    else:
                        # 录制服务停止失败
                        raise MockServerRecordStoppedError(
                            'Mock record stop error, status_code: {}!'.format(stop_response.status_code)
                        )


if __name__ == "__main__":
    run_mock_server()
    # with MockServerManage(cmd) as wm:
    #     print('start mock server...')
    #     time.sleep(30)
    #     # wm.stop()
    #     # print(wm.start().__subprocess.stdout.readlines())
    #     print('end!')
    # mock_record = MockRecordManage(base_url, wiremock_url, wiremock_port)
    # mock_record.start_record()
    # time.sleep(30)
    # mock_record.stop_record()
