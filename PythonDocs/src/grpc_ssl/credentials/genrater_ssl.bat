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

