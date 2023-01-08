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