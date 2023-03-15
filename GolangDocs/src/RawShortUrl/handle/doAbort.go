package handle

import (
	"net"

	"github.com/Bean-jun/rawUrl/internal/request"
	"github.com/Bean-jun/rawUrl/internal/response"
)

// Abort 网站异常
func Abort(headers *request.ReqHeader, conn net.Conn) {
	defer conn.Close()
	// 写入响应头
	responseHeader := response.InitHttpResponseHeader(headers)
	responseHeader = response.SetResponseHeaderCode(responseHeader, 400)
	// 拼装响应头
	responseBody := response.ResponseToString(responseHeader, "")
	// 设置响应体
	_, err := conn.Write([]byte(responseBody.String()))
	if err != nil {
		return
	}
}
