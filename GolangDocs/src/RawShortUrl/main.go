package main

import (
	"encoding/json"
	"log"
	"net"
	"os"
	"time"

	"github.com/Bean-jun/rawUrl/handle"
	"github.com/Bean-jun/rawUrl/internal"
	"github.com/Bean-jun/rawUrl/internal/request"
)

func init() {
	var fileData []byte
	ok := internal.Exist(internal.LocalDB)
	if !ok {
		file, err := os.OpenFile(internal.LocalDB, os.O_APPEND|os.O_CREATE|os.O_RDWR, 0777)
		if err != nil {
			panic(err.Error())
		}
		file.Close()
	}
	fileData, err := os.ReadFile(internal.LocalDB)
	if err != nil {
		panic(err.Error())
	}
	err = json.Unmarshal(fileData, &internal.UrlMap.Url)
	if err != nil {
		log.Println("Unmarshal", err.Error())
	}
}

func main() {
	// 监听端口
	listen, err := net.Listen("tcp", internal.Port)
	if err != nil {
		log.Println("create listen error ", err.Error())
	}

	go internal.WriteUrlToDB(internal.LocalDB)

	for {
		// 等待获取一个连接对象
		conn, err := listen.Accept()
		if err != nil {
			log.Println("create conn error", err.Error())
		}
		// 基于协程进行当前连接对象的处理
		go Handle(conn)
	}
}

func Handle(conn net.Conn) {
	start := time.Now()
	header := make([]byte, 0, internal.MaxHeaderSize)
	for {
		headerRead := make([]byte, internal.ReadHeaderSize)
		n, err := conn.Read(headerRead)
		if err != nil {
			return
		}

		header = append(header, headerRead...)
		log.Println("read data value length: ", n)
		if n < internal.ReadHeaderSize {
			break
		}
	}
	log.Println("use time total: ", time.Since(start))
	// 解析请求头
	headers, body := request.ParseHttpHeader(header)

	m, _ := request.ParseRequestBody(headers, body)

	log.Println(m)

	switch headers.Method {
	case "GET":
		handle.DoGet(headers, nil, conn)
	case "POST":
		handle.DoPost(headers, m, conn)
	default:
		handle.Abort(headers, conn)
	}
}
