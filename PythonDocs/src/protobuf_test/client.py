from proto.hello_pb2 import HelloRequest

request = HelloRequest()
request.name = "tom"
# 序列化为字符串
to_str = request.SerializeToString()
print(to_str)

request2 = HelloRequest()
ret = request2.FromString(to_str)
print(ret.name)