package response

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/Bean-jun/rawUrl/internal"
	"github.com/Bean-jun/rawUrl/internal/request"
)

// RespHeaderLine 响应头首行
type RespHeaderLine struct {
	Protocol string
	Code     int
	Desc     string
}

// RespHeaderBody 响应头body
type RespHeaderBody struct {
	Body map[string]interface{}
}

// RespHeader 响应头
type RespHeader struct {
	RespHeaderLine
	RespHeaderBody
}

// InitHttpResponseHeader 写入响应头
func InitHttpResponseHeader(r *request.ReqHeader) *RespHeader {
	return &RespHeader{
		RespHeaderLine{Protocol: r.Protocol},
		RespHeaderBody{map[string]interface{}{
			"Server": "Go1.19",
		}},
	}
}

// SetResponseHeaderCode 设置响应头
func SetResponseHeaderCode(resp *RespHeader, code int) *RespHeader {
	resp.Code = internal.HttpStatusCodeMap[code].Code
	resp.Desc = internal.HttpStatusCodeMap[code].Desc
	return resp
}

// ResponseToString 响应转string
func ResponseToString(r *RespHeader, body string) *strings.Builder {
	// 设置响应体长度
	r.Body["Content-Length"] = strconv.Itoa(len(body))

	header := &strings.Builder{}
	header.WriteString(fmt.Sprintf("%s %d %s\r\n", r.Protocol, r.Code, r.Desc))
	for k, v := range r.Body {
		header.WriteString(fmt.Sprintf("%s: %s\r\n", k, v.(string)))
	}
	header.WriteString("\r\n")
	header.WriteString(body)
	return header
}
