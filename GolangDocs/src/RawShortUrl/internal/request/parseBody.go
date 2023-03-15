package request

import (
	"errors"
	"regexp"
	"strings"
)

const (
	FormDataKeyStr = "multipart/form-data; "
	FormDataPerfix = "Content-Disposition"
	FormDataStr    = "Content-Disposition: form-data; name="
	FormDataRegex  = `Content-Disposition: form-data; name="(.*)"`
)

var Re = regexp.MustCompile(FormDataRegex)

// ParseBody 解析请求体
func ParseBody(ctype, body string) (map[string]string, error) {
	//application/x-www-form-urlencoded
	if ctype == "application/x-www-form-urlencoded" {
		return ParseFormUrlencoded(body), nil
	}

	// multipart/form-data
	if strings.HasPrefix(ctype, "multipart/form-data") {
		splitKey := FormDataKey(ctype)
		return ParseFormData(splitKey, body), nil
	}

	return nil, errors.New("解析请求体异常")
}

// ParseFormUrlencoded application/x-www-form-urlencoded
func ParseFormUrlencoded(bodyStr string) map[string]string {
	bodyStrSlice := strings.Split(bodyStr, "&")
	bodyMap := map[string]string{}
	for _, bodykv := range bodyStrSlice {
		kvSlice := strings.Split(bodykv, "=")
		if len(kvSlice) >= 2 {
			bodyMap[kvSlice[0]] = kvSlice[1]
		} else {
			bodyMap[kvSlice[0]] = ""
		}
	}
	return bodyMap
}

// FormDataKey form-data切割key
func FormDataKey(s string) string {
	key := s[len(FormDataKeyStr):]
	return "--" + key[len("boundary="):]
}

// ParseFormData multipart/form-data
func ParseFormData(splitKey, bodyStr string) map[string]string {
	bodyStrSlice := strings.Split(bodyStr, splitKey)
	bodyMap := map[string]string{}
	for _, body := range bodyStrSlice {
		if body == "" {
			continue
		}
		body = strings.Trim(body, "\r\n")
		if !strings.HasPrefix(body, FormDataPerfix) {
			continue
		}
		matched := Re.FindStringSubmatch(body)
		if len(matched) < 2 {
			continue
		}
		key := matched[1]
		trimStr := FormDataStr + "\"" + key + "\""
		value := body[len(trimStr):]
		bodyMap[key] = value
	}
	return bodyMap
}
