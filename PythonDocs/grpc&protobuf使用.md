### 一、安装protobuf工具

1. 编译工具

    下载地址： [https://github.com/protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf)

2. python package

    `pip install protobuf`

### 二、python使用protobuf

1. 编辑protobuf文件

    ```proto
    syntax = "proto3";

    package hello;

    message HelloRequest {
        string name = 1;
    }
    ```

2. 编译protobuf文件

    ```shell
    protoc xxx.proto
    ```

3. 进行调用

    ```python
    # PythonDocs/src/protobuf_test/client.py
    from proto.hello_pb2 import HelloRequest

    request = HelloRequest()
    request.name = "tom"
    # protobuf序列化
    to_str = request.SerializeToString()
    print(to_str)

    request2 = HelloRequest()
    # 将protobuf序列化的结果转换为python对象
    ret = request2.FromString(to_str)
    print(ret.name)
    ```



### 三、python使用protobuf&grpc

1. 安装依赖环境

    ```shell
    pip install grpcio
    pip install grpcio_tools
    ```

2. 编辑protobuf文件

    ```protobuf
    syntax="proto3";

    service Greeter {
        rpc SayHello (HelloRequest) returns (HelloReply){};
    }

    message HelloRequest{
        string name = 1;
    }

    message HelloReply{
        string message = 1;
    }
    ```

3. 通过protobuf文件生产对应python文件

    ```shell
    # --python_out 生成的文件地址 --grpc_python_out生成的grpc文件地址 -I protobuf文件地址
    python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I . hello.proto
    ```

4. 编辑server端

    ```python
    # PythonDocs/src/grpc_hello_py/server.py
    from concurrent import futures

    import grpc
    from proto import hello_pb2, hello_pb2_grpc


    class Greeter(hello_pb2_grpc.GreeterServicer):

        def SayHello(self, request, context):
            return hello_pb2.HelloReply(message=f"你好，{request.name}")


    if __name__ == "__main__":
        # 创建server
        server = grpc.server(futures.ThreadPoolExecutor(10))
        # 注册至server
        hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        # 启动server
        server.add_insecure_port("localhost:5000")
        server.start()
        server.wait_for_termination()
    ```

5. 编辑client端

    ```python
    # PythonDocs/src/grpc_hello_py/client.py
    import grpc
    from proto import hello_pb2, hello_pb2_grpc


    if __name__ == "__main__":
        with grpc.insecure_channel("localhost:5000") as channel:
            stub = hello_pb2_grpc.GreeterStub(channel)
            response = stub.SayHello(hello_pb2.HelloRequest(name="tom"))
            print(response.message)
    ```

### 四、使用ssl进行grpc加密通信 (项目地址：./src/grpc_ssl)

1. 生成证书秘钥

    ```shell
    @REM key： 服务器上的私钥文件，用于对发送给客户端数据的加密，以及对从客户端接收到数据的解密。
    @REM csr： 证书签名请求文件，用于提交给证书颁发机构（CA）对证书签名。
    @REM crt： 由证书颁发机构（CA）签名后的证书，或者是开发者自签名的证书，包含证书持有人的信息，持有人的公钥，以及签署者的签名等信息。
    @REM pem： 是基于Base64编码的证书格式，扩展名包括PEM、CRT和CER。
    @REM Common Name (e.g. server FQDN or YOUR name) []: 此栏目必填，否则grpc查找无法匹配到这个域名

    @REM ----------------------------


    @REM 生成ca根证书
    @REM 生成密钥
    openssl genrsa -out ca.key 4096
    @REM 生成密钥签发请求
    openssl req -new -sha256 -key ca.key -out ca.csr
    @REM 生成根证书
    openssl x509 -req -days 3650 -in ca.csr -signkey ca.key -out ca.crt


    @REM ----------------------------

    @REM 生成服务端证书
    openssl genrsa -out server.key 2048
    openssl req -new -sha256 -key server.key -out server.csr
    @REM  用CA证书生成服务端证书
    openssl x509 -req -days 3650 -CA ca.crt -CAkey ca.key -CAcreateserial -in server.csr -out server.pem
    ```

2. 改造server端
    
    ```python
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(UserService(), server)
    server.add_secure_port('[::]:50051', grpc.ssl_server_credentials(
        [(_load_credential_from_file("credentials/server.key"),
        _load_credential_from_file("credentials/server.pem"))]
    ))
    # server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    ```

3. 改造client端

    ```python
    # with grpc.insecure_channel('localhost:50051') as channel:
    with grpc.secure_channel('localhost:50051', grpc.ssl_channel_credentials(
            _load_credential_from_file("credentials/server.pem")
    )) as channel:
        userService = UserServiceStub(channel)
        res = userService.Login(RequestLogin(username="test", password="<PASSWORD>"))
        print(res.msg, res.valid)
        print(res)
    ```