package internal

import (
	"net/url"
	"sync"
)

var (
	Schema         = "http"
	Host           = "127.0.0.1"
	Port           = ":7256"
	MaxHeaderSize  = 1 << 10
	ReadHeaderSize = 1 << 8
	IndexHtml      = "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <title>短连接生成器</title>\n</head>\n<body>\n<form action=\"/\" method=\"post\">\n    <label>\n        <input type=\"text\" name=\"url\"/>\n    </label>\n    <input type=\"submit\" value=\"提交\">\n</form>\n</body>\n</html>"
	PathUnescape   = url.PathUnescape
	LocalDB        = "short.json"
	UrlMap         = struct {
		L   sync.RWMutex
		Url map[string]string
	}{
		Url: map[string]string{},
	}
	HttpStatusCodeMap = HttpStatusMap{
		100: HttpStatus{Code: 100, Desc: "Continue"},
		200: HttpStatus{Code: 200, Desc: "OK"},
		301: HttpStatus{Code: 301, Desc: "Moved Permanently"},
		400: HttpStatus{Code: 400, Desc: "Bad Request"},
		403: HttpStatus{Code: 403, Desc: "Forbidden"},
		404: HttpStatus{Code: 404, Desc: "Not Found"},
		405: HttpStatus{Code: 405, Desc: "Method Not Allowed"},
		500: HttpStatus{Code: 500, Desc: "Internal Server Error"},
		502: HttpStatus{Code: 502, Desc: "Bad Gateway"},
	}
)
