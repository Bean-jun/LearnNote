package frame

/*
对请求handler(w http.ResponseWriter, r *http.Request)进行封装
*/

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// H 约束用户传入结构格式
type H map[string]interface{}

type Context struct {
	Writer     http.ResponseWriter
	Request    *http.Request
	Path       string
	Method     string
	Params     map[string]string // 获取路径参数
	StatusCode int

	handlers []HandlerFunc // 保存中间件 方便中间件的后续调用
	index    int

	engine *Engine //可通过Context访问engine
}

func newContext(w http.ResponseWriter, r *http.Request) *Context {
	return &Context{
		Writer:  w,
		Request: r,
		Path:    r.URL.Path,
		Method:  r.Method,
		index:   -1,
	}
}

// Next 中间件
func (c *Context) Next() {
	c.index++
	for ; c.index < len(c.handlers); c.index++ {
		c.handlers[c.index](c)
	}
}

// PostForm 获取请求体参数
func (c *Context) PostForm(key string) string {
	return c.Request.FormValue(key)
}

// Query 获取查询参数
func (c *Context) Query(key string) string {
	return c.Request.URL.Query().Get(key)

} // Param 获取路径参数
func (c *Context) Param(key string) string {
	v, ok := c.Params[key]
	if ok {
		return v
	}
	return ""
}

// Status 设置相应状态码
func (c *Context) Status(code int) {
	c.StatusCode = code
	c.Writer.WriteHeader(code)
}

// SetHeader 设置相应头
func (c *Context) SetHeader(key, value string) {
	c.Writer.Header().Set(key, value)
}

// Error 相应错误
func (c *Context) Error(code int) {
	c.SetHeader("Content-Type", "text/plain")
	c.Status(code)
}

// String 相应字符串
func (c *Context) String(code int, format string, values ...interface{}) {
	c.SetHeader("Content-Type", "text/plain")
	c.Status(code)
	_, err := c.Writer.Write([]byte(fmt.Sprintf(format, values...)))
	if err != nil {
		c.Error(500)
	}
}

// Json 相应Json
func (c *Context) Json(code int, obj interface{}) {
	c.SetHeader("Content-Type", "application/json")
	c.Status(code)
	encoder := json.NewEncoder(c.Writer)
	err := encoder.Encode(obj)
	if err != nil {
		c.Error(500)
	}
}

// Data 相应Data
func (c *Context) Data(code int, data []byte) {
	c.Status(code)
	_, err := c.Writer.Write(data)
	if err != nil {
		c.Error(500)
	}
}

// HTML 相应HTML
func (c *Context) HTML(code int, name string, data interface{}) {
	c.SetHeader("Content-Type", "text/html")
	c.Status(code)
	err := c.engine.htmlTemplates.ExecuteTemplate(c.Writer, name, data)
	if err != nil {
		c.Error(500)
	}
}
