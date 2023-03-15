package request

import (
	"bytes"
	"errors"
	"regexp"
	"strconv"
	"strings"
)

// ReqHeaderLine 请求头首行
type ReqHeaderLine struct {
	Method   string
	Url      string
	Protocol string
}

// ReqHeaderBody 请求头body
type ReqHeaderBody struct {
	Body map[string]interface{}
}

// ReqHeader 请求头
type ReqHeader struct {
	ReqHeaderLine
	ReqHeaderBody
}

// ParseHttpRequestFirstLine 解析请求头首行
func ParseHttpRequestFirstLine(line []byte) *ReqHeaderLine {
	re := regexp.MustCompile(`([A-Z]+)\s(/.*)\s(HTTP/1.[0-1]+)$`)
	matched := re.FindStringSubmatch(string(line))
	if len(matched) != 4 {
		panic(errors.New("parse request header error"))
	}
	return &ReqHeaderLine{
		Method:   matched[1],
		Url:      matched[2],
		Protocol: matched[3],
	}
}

// ParseHttpRequestLine 解析请求头
func ParseHttpRequestLine(lines ...[]byte) *ReqHeaderBody {
	var body = map[string]interface{}{}
	for _, line := range lines {
		lineSlice := strings.Split(string(line), ": ")
		body[lineSlice[0]] = lineSlice[1]
	}
	return &ReqHeaderBody{
		Body: body,
	}
}

// ParseHttpHeader 解析请求头
func ParseHttpHeader(reqData []byte) (*ReqHeader, *bytes.Buffer) {
	reqHeaderWithBody := bytes.Split(reqData, []byte("\r\n\r\n")) // form-data会被切割-导致不完整
	reqHeader := bytes.Split(reqHeaderWithBody[0], []byte("\r\n"))
	if len(reqHeader) < 1 {
		panic(errors.New("request header parse error"))
	}
	reqBody := &bytes.Buffer{}
	for _, body := range reqHeaderWithBody[1:] {
		reqBody.Write(body)
	}
	return &ReqHeader{
		ReqHeaderLine: *ParseHttpRequestFirstLine(reqHeader[0]),
		ReqHeaderBody: *ParseHttpRequestLine(reqHeader[1:]...),
	}, reqBody
}

// ParseRequestBody 解析请求体
func ParseRequestBody(r *ReqHeader, bodyBuffer *bytes.Buffer) (map[string]string, error) {
	body := bodyBuffer.Bytes()
	value := 0
	if v, ok := r.Body["Content-Length"]; !ok {
		return nil, errors.New("error")
	} else {
		value, _ = strconv.Atoi(v.(string))
	}
	bodyStr := string(body[:value])

	cType, ok := r.Body["Content-Type"]
	if !ok {
		return nil, errors.New("error Content-Type")
	}

	return ParseBody(cType.(string), bodyStr)
}
