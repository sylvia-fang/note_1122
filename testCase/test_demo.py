import unittest
from client_stub import fileAppStub
import json
import time
from httpStubFramework.httpCommon import HttpCommon
from common.customsLog import case_log_class, info_log
from common.read_yml import ReadYaml
from business_common.apiBusiness import ApiBusiness


@case_log_class
class TestPro(unittest.TestCase):
    rY = ReadYaml()
    apiBusiness = ApiBusiness()
    env_config = rY.env_yaml()
    host = env_config['host']

    def testCase01_demo(self):
        """主流程"""
        file_id = '121'
        user_id = '8771'

        info_log("前置：清空文件协作用户")
        self.apiBusiness.clear_file_members(file_id)

        info_log("请求被测服务接口")
        data = {
            "file_id": file_id,
            "status": "edit"
        }
        headers = {
            "Cookie": f"user_id={user_id}",
            "Content-Type": "application/json"
        }

        hc = HttpCommon()
        hc.thread_run_requests(method="POST", url=self.host + "/edit", json=data, headers=headers)

        info_log("被测服务校验文件是否存在，请求file服务(桩)，桩接收消息")
        receive_msg = fileAppStub.receive_msg()
        info_log("校验fileApp桩收到的消息")
        receive_body = receive_msg['body']
        self.assertEqual(1, len(receive_body.keys()))  # 校验请求体没有其他字段
        self.assertEqual(file_id, receive_body['file_id'])  # 校验file_id的值和对外接口输入的一致
        self.assertEqual('file', receive_msg['path'])  # 校验接口请求的路由信息是否正确
        self.assertEqual('GET', receive_msg['method'])  # 校验http的请求方式是否正确

        info_log("fileApp桩服务回复正常消息")
        send_data = {
            "body": {"msg": "success"},
            "status_code": 200
        }
        fileAppStub.send_msg(send_data)

        self.assertEqual(200, hc.status_code)
        self.assertEqual('edit success', json.loads(hc.res_text)['msg'])

    def testCase02_demo(self):
        """三方服务处理超时，校验被测服务超时机制"""
        file_id = '121'
        user_id = '8771'

        info_log("前置：清空文件协作用户")
        self.apiBusiness.clear_file_members(file_id)

        info_log("请求被测服务接口")
        data = {
            "file_id": file_id,
            "status": "edit"
        }
        headers = {
            "Cookie": f"user_id={user_id}",
            "Content-Type": "application/json"
        }

        hc = HttpCommon()
        hc.thread_run_requests(method="POST", url=self.host + "/edit", json=data, headers=headers)

        info_log("被测服务校验文件是否存在，请求file服务(桩)，桩接收消息")
        receive_msg = fileAppStub.receive_msg()
        info_log("校验fileApp桩收到的消息")
        receive_body = receive_msg['body']
        self.assertEqual(1, len(receive_body.keys()))  # 校验请求体没有其他字段
        self.assertEqual(file_id, receive_body['file_id'])  # 校验file_id的值和对外接口输入的一致
        self.assertEqual('file', receive_msg['path'])  # 校验接口请求的路由信息是否正确
        self.assertEqual('GET', receive_msg['method'])  # 校验http的请求方式是否正确

        time.sleep(4)
        info_log("fileApp桩服务回复正常消息")
        send_data = {
            "body": {"msg": "success"},
            "status_code": 200
        }
        fileAppStub.send_msg(send_data)

        self.assertEqual(504, hc.status_code)
        self.assertEqual('SERVER TIMEOUT', json.loads(hc.res_text)['msg'])

    def testCase03_demo(self):
        """三方服务返回异常状态码403"""
        file_id = '121'
        user_id = '8771'

        info_log("前置：清空文件协作用户")
        self.apiBusiness.clear_file_members(file_id)

        info_log("请求被测服务接口")
        data = {
            "file_id": file_id,
            "status": "edit"
        }
        headers = {
            "Cookie": f"user_id={user_id}",
            "Content-Type": "application/json"
        }

        hc = HttpCommon()
        hc.thread_run_requests(method="POST", url=self.host + "/edit", json=data, headers=headers)

        info_log("被测服务校验文件是否存在，请求file服务(桩)，桩接收消息")
        receive_msg = fileAppStub.receive_msg()
        info_log("校验fileApp桩收到的消息")
        receive_body = receive_msg['body']
        self.assertEqual(1, len(receive_body.keys()))  # 校验请求体没有其他字段
        self.assertEqual(file_id, receive_body['file_id'])  # 校验file_id的值和对外接口输入的一致
        self.assertEqual('file', receive_msg['path'])  # 校验接口请求的路由信息是否正确
        self.assertEqual('GET', receive_msg['method'])  # 校验http的请求方式是否正确

        info_log("fileApp桩服务回复处理异常，状态码403")
        send_data = {
            "body": {"msg": "fail"},
            "status_code": 403
        }
        fileAppStub.send_msg(send_data)

        self.assertEqual(500, hc.status_code)
        self.assertEqual('SERVER ERROR', json.loads(hc.res_text)['msg'])
