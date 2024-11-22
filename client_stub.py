from httpStubFramework.httpServerOperate import StubOperate

# init stub
fileAppConfig = {
    "http_port": 8771,
    "socket_client_port": 8772,
    "socket_server_port": 8773
}

fileAppStub = StubOperate(fileAppConfig["http_port"], fileAppConfig["socket_client_port"],
                          fileAppConfig["socket_server_port"])

print("init stub")
