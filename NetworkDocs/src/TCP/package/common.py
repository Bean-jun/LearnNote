import struct
import threading


HeaderLength = 12
__format = "!3I"
local = threading.local()
local.stroage = bytes()


def to_bytes(msg):
    if isinstance(msg, bytes):
        return msg
    if isinstance(msg, str):
        return msg.encode("utf-8")
    return str(msg).encode("utf-8")


def package(msg, version=1, cmd=100):
    __body = to_bytes(msg)
    __header = [version, len(__body), cmd]
    header = struct.pack(__format, *__header)
    body = header + __body
    return body


def unpackage(msg):
    local.stroage += msg
    if len(local.stroage) < HeaderLength:
        return

    # 解析头
    __header = local.stroage[:HeaderLength]
    version, body_len, _ = struct.unpack(__format, __header)
    if len(local.stroage) < HeaderLength + body_len:
        return
    # 获取body
    body = local.stroage[HeaderLength:HeaderLength+body_len]

    # 将当前存储数据进行释放，（粘包数据自动释放）
    local.stroage = local.stroage[HeaderLength+body_len:]

    return body


def send_msg(sock, msg):
    sock.send(package(msg))


def user_send_msg(sock):
    to = input(">>>:")
    if to == "":
        return
    send_msg(sock, to)


def get_msg(sock):
    body = b""
    while True:
        msg = sock.recv(1024)
        body = unpackage(msg)
        if not body:
            return
        print("recv:", body.decode("utf-8"))
        return