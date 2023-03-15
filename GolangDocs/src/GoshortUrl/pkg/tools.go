package pkg

import (
	"encoding/base64"
	"errors"
	"fmt"
	"net/http"
	"time"
)

func Get(keys string) string {
	Url.L.RLock()
	defer Url.L.RUnlock()
	if value, ok := Url.UrlMap[keys]; !ok {
		return ""
	} else {
		return value
	}
}

func Set(keys, value string) error {
	if Get(keys) != "" {
		return errors.New("当前keys已存在")
	}
	Url.L.Lock()
	defer Url.L.Unlock()
	Url.UrlMap[keys] = value
	return nil
}

// ToResponse 响应前端
func ToResponse(w http.ResponseWriter, msg string) {
	_, err := w.Write([]byte(msg))
	if err != nil {
		return
	}
}

// AddPrefix 添加站点前缀
func AddPrefix(url string) string {
	return fmt.Sprintf("%s://%s%s/?url=%s", Schema, Host, Port, url)
}

// GenerateShort 生成短连接
func GenerateShort() func() string {
	nums := 97
	return func() string {
		val := fmt.Sprintf("%d-%s", nums, time.Now().Format("2006-01-02 15:04:05"))
		val = base64.StdEncoding.EncodeToString([]byte(val))
		nums += 1
		return val
	}
}
