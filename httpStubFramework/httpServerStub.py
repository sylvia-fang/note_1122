import threading
from flask import Flask, request
from werkzeug.serving import make_server
import socket
import json
from httpStubFramework.threadCount import server_lst
import os
import signal


clientSocket = None


class HttpStub:
    app = Flask(__name__)

    def __init__(self, port, socket_client_port, socket_server_port):
        self.client_socket = None
        self.port = port
        self.socket_client_port = socket_client_port
        self.socket_server_port = socket_server_port

    def http_server(self):
        """桩服务实例化socket客户端"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_address = ('localhost', self.socket_client_port)
        self.client_socket.bind(client_address)
        server_address = ("localhost", self.socket_server_port)
        self.client_socket.connect(server_address)

        server_lst.add("http_stub")
        return self.client_socket

    @staticmethod
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    def msg_collect(path):
        """http桩，兼容所有路由和请求方式"""
        try:
            re_method = request.method
            if path == 'shutdown' and re_method == 'POST':
                os.kill(os.getpid(), signal.SIGINT)
                return 'Server shutting down...', 200
            re_headers = request.headers
            re_cookies = request.cookies
            if re_method == "GET":

                re_data = request.args
            else:
                re_data = request.get_json()
        except Exception as e:
            print(e)
            return {}, 888

        receive_msg = {
            "body": dict(re_data),
            "headers": dict(re_headers),
            "cookies": dict(re_cookies),
            "path": path,
            "method": re_method
        }
        message = json.dumps(receive_msg)
        clientSocket.sendall(message.encode("utf-8"))

        data = clientSocket.recv(1024).decode("utf-8")
        send_data = json.loads(data)
        if send_data is not {}:
            send_response = send_data["body"]
            send_status_code = send_data["status_code"]
            return send_response, send_status_code

        else:
            pass  # 不处理

    def server_run(self):
        """http桩启动"""
        global clientSocket
        clientSocket = self.http_server()
        server = make_server('127.0.0.1', self.port, self.app)
        server.serve_forever()


