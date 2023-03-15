package handle

import (
	"net"
	"strings"

	"github.com/Bean-jun/rawUrl/internal"
	"github.com/Bean-jun/rawUrl/internal/request"
	"github.com/Bean-jun/rawUrl/internal/response"
)

// GetRequestUrlPath 获取请求路径
func GetRequestUrlPath(r *request.ReqHeader) string {
	return r.Url
}

func DoGet(headers *request.ReqHeader, body map[string]string, conn net.Conn) {
	defer conn.Close()
	responseHeader := response.InitHttpResponseHeader(headers)
	responseHeader = response.SetResponseHeaderCode(responseHeader, 200)
	var responseBody *strings.Builder

	redirectKey := GetRequestUrlPath(headers)
	// 返回首页
	if redirectKey == "/" {
		responseBody = response.ResponseToString(responseHeader, internal.IndexHtml)
	} else {
		redirectValue := internal.UrlGet(strings.Trim(redirectKey, "/"))
		responseHeader.Body["Location"] = redirectValue
		responseHeader = response.SetResponseHeaderCode(responseHeader, 301)
		responseBody = response.ResponseToString(responseHeader, "")
	}
	_, err := conn.Write([]byte(responseBody.String()))
	if err != nil {
		return
	}
}
