package pkg

import "sync"

var (
	Schema = "http"
	Host   = "127.0.0.1"
	Port   = ":8080"
	Url    = struct {
		UrlMap map[string]string
		L      sync.RWMutex // 为Url加锁，避免并发问题
	}{
		UrlMap: map[string]string{}, // 对map先做初始化，避免后续使用异常
	}
	ShowUrl  = true
	Generate = GenerateShort()
)
