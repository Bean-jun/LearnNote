import socket
import json

request = {
    "id": 0,
    "params": [{"x":10, "y":50}],  # 参数要对应上Args结构体
    "method": "ServiceA.Add"
}

client = socket.create_connection(("127.0.0.1", 9000),5)
client.sendall(json.dumps(request).encode())

rsp = client.recv(1024)
rsp = json.loads(rsp.decode())
print(rsp)