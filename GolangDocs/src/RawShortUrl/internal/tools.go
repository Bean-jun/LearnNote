package internal

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

// UrlGet 获取Url
func UrlGet(key string) string {
	UrlMap.L.RLock()
	defer UrlMap.L.RUnlock()
	if value, ok := UrlMap.Url[key]; !ok {
		return ""
	} else {
		return value
	}
}

// UrlSet 设置Url
func UrlSet(key, value string) bool {
	if _, ok := UrlMap.Url[key]; ok {
		return false
	}
	UrlMap.L.Lock()
	defer UrlMap.L.Unlock()
	if !strings.HasPrefix(value, "http") {
		value = "http://" + value
	}
	UrlMap.Url[key] = value
	return true
}

// HttpStatus http状态码
type HttpStatus struct {
	Code int
	Desc string
}

// HttpStatusMap http状态码集合
type HttpStatusMap map[int]HttpStatus

// Exist 文件是否存在
func Exist(path string) bool {
	if _, err := os.Stat(path); err != nil {
		return false
	} else {
		return true
	}
}

// GenerateRandomKey 生成一个随机key
func GenerateRandomKey() string {
	key := fmt.Sprintf("%s-%s", strconv.Itoa(rand.Int()), time.Now().Format("2006-01-02 15:04:05"))
	return base64.StdEncoding.EncodeToString([]byte(key))
}

// WriteUrlToDB 保存数据
func WriteUrlToDB(db string) {
	for {
		time.Sleep(time.Second * 2)
		url, err := json.Marshal(UrlMap.Url)
		if err != nil {
			log.Println("Marshal", err.Error())
			continue
		}
		err = os.WriteFile(db, url, 0777)
		if err != nil {
			log.Println("WriteFile", err.Error())
		}
	}
}
