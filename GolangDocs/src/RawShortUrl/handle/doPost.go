package handle

import (
	"fmt"
	"net"
	"strings"

	"github.com/Bean-jun/rawUrl/internal"
	"github.com/Bean-jun/rawUrl/internal/request"
	"github.com/Bean-jun/rawUrl/internal/response"
)

func DoPost(headers *request.ReqHeader, body map[string]string, conn net.Conn) {
	defer conn.Close()
	responseHeader := response.InitHttpResponseHeader(headers)
	responseHeader.Body["Content-Type"] = "text/html;charset=utf-8"
	responseHeader = response.SetResponseHeaderCode(responseHeader, 200)
	var responseBody *strings.Builder

	if v, ok := body["url"]; !ok {
		responseHeader = response.SetResponseHeaderCode(responseHeader, 400)
		responseBody = response.ResponseToString(responseHeader, "地址填写异常")
	} else {
		key := internal.GenerateRandomKey()
		pathUnescape, err := internal.PathUnescape(v)
		if err != nil {
			panic(err)
		}
		status := internal.UrlSet(key, pathUnescape)
		if !status {
			responseBody = response.ResponseToString(responseHeader, "地址配置重复")
		} else {
			respKey := fmt.Sprintf("%s://%s%s/%s", internal.Schema, internal.Host, internal.Port, key)
			responseBody = response.ResponseToString(responseHeader, respKey)
		}
	}
	_, err := conn.Write([]byte(responseBody.String()))
	if err != nil {
		return
	}
}
