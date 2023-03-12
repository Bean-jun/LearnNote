package main

import (
	"html/template"
	"log"
	"strconv"
	"strings"
	"time"
	"webframe/frame"
)

func m1() frame.HandlerFunc {
	return func(c *frame.Context) {
		t1 := time.Now()
		c.Next()
		log.Println("接口请求时间:", time.Now().Sub(t1))
	}
}

// ===========================分割线===================================
func hello(c *frame.Context) {
	time.Sleep(time.Second * 3)
	c.Json(200, frame.H{
		"msg":    "hello world",
		"path":   c.Path,
		"method": c.Method,
		"query":  c.Query("page"),
		"param":  c.Param("name"),
	})
}

func index(c *frame.Context) {
	c.HTML(200, "index.tmpl", frame.H{
		"content": "this is template render result",
	})
}

func Books(c *frame.Context) {
	books := [3]string{"go", "python", "java"}
	page, _ := strconv.Atoi(c.Param("page"))
	c.Json(200, frame.H{
		"books": books[page],
	})
}

func main() {
	engine := frame.NewEngine()
	engine.SetFuncMap(template.FuncMap{
		"upper": func(s string) string { return strings.ToUpper(s) },
	})
	engine.LoadHTMLGlob("templates/*")
	engine.Static("/abc", "./static")
	api := engine.Group("/api")
	api.Use(m1(), frame.Recovery())
	{
		api.GET("/hello/:name", hello)
		api.GET("/books/:page", Books)
	}
	engine.GET("/index", index)
	log.Fatal(engine.Run(":8080"))
}
