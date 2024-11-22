from httpStubFramework.httpServerStub import HttpStub
import threading
import requests
import socket
import json
import time
from httpStubFramework.threadCount import server_lst


class StubOperate:
    def __init__(self, port, socket_client_port, socket_server_port):
        self.port = port
        self.socket_client_port = socket_client_port
        self.socket_server_port = socket_server_port
        self.server_socket = None
        self.client_socket = None

    def server_socket_start(self):
        """桩socket客户端的启动"""
        self.client_socket, client_address = self.server_socket.accept()
        server_lst.add("socket_server")

    def start_stub(self):
        """http桩初始化"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', self.socket_server_port)
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)

        http_stub = HttpStub(self.port, self.socket_client_port, self.socket_server_port)
        t = threading.Thread(target=http_stub.server_run)
        t2 = threading.Thread(target=self.server_socket_start)

        t.start()
        time.sleep(2)
        t2.start()
        time.sleep(2)

    def shutdown_stub(self):
        """http桩下线"""
        requests.post(url=f"http://127.0.0.1:{self.port}/shutdown", timeout=3)
        self.client_socket.close()
        self.server_socket.close()

    def receive_msg(self):
        """http桩mock消息接收"""
        data = self.client_socket.recv(1024).decode("utf-8")
        return json.loads(data)

    def send_msg(self, data):
        """http桩mock消息发送"""
        data = json.dumps(data)
        self.client_socket.sendall(data.encode("utf-8"))
        time.sleep(2)
