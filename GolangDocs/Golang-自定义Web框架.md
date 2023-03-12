**相关源码见`GolangDocs\src\webframe`目录**

## 0x01 基础的http请求接口实现

```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

func hello(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Method)
	_, err := w.Write([]byte("hello"))
	if err != nil {
		panic(err)
	}
}

func main() {
	http.HandleFunc("/hello", hello)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## 0x02 自定义Handler-实现ServerHTTP方法

```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

// Handler 写在这里就是醒目作用 官方已自定义
type Handler interface {
	ServeHTTP(http.ResponseWriter, *http.Request)
}

type Engine struct{}

// ServeHTTP 实现此方法即可将此解构丢入ListenAndServe
func (e *Engine) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Method, r.URL.Path)
	switch r.URL.Path {
	case "/hello":
		_, err := w.Write([]byte(("hello")))
		if err != nil {
			return
		}
	case "/world":
		_, err := w.Write([]byte(("world")))
		if err != nil {
			return
		}
	}
}

func main() {
	log.Fatal(http.ListenAndServe(":8080", new(Engine)))
}
```

## 0x03 仿gin,可自定义请求动作

```go
package main

import (
	"fmt"
	"log"
	"net/http"
)

// HandlerFunc 定义HandlerFunc用于设置用户请求约束
type HandlerFunc func(http.ResponseWriter, *http.Request)

type Engine struct {
	router map[string]HandlerFunc
}

func NewEngine() *Engine {
	return &Engine{
		router: make(map[string]HandlerFunc),
	}
}
func (e *Engine) AddRoute(method, patten string, handler HandlerFunc) {
	keys := method + "_" + patten
	e.router[keys] = handler
}

func (e *Engine) GET(patten string, handler HandlerFunc) {
	e.AddRoute("GET", patten, handler)
}

func (e *Engine) POST(patten string, handler HandlerFunc) {
	e.AddRoute("POST", patten, handler)
}

func (e *Engine) PUT(patten string, handler HandlerFunc) {
	e.AddRoute("PUT", patten, handler)
}

func (e *Engine) DELETE(patten string, handler HandlerFunc) {
	e.AddRoute("DELETE", patten, handler)
}

func (e *Engine) Any(patten string, handler HandlerFunc) {
	e.AddRoute("GET", patten, handler)
	e.AddRoute("POST", patten, handler)
	e.AddRoute("PUT", patten, handler)
	e.AddRoute("DELETE", patten, handler)
}

// ServeHTTP 实现此方法即可将此解构丢入ListenAndServe
func (e *Engine) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Method, r.URL.Path)
	keys := r.Method + "_" + r.URL.Path
	if handler, ok := e.router[keys]; !ok {
		_, err := w.Write([]byte("404 NOT FOUND"))
		if err != nil {
			return
		}
	} else {
		handler(w, r)
	}
}

// Run 用户调用Run实现server启动
func (e *Engine) Run(addr string) error {
	return http.ListenAndServe(addr, e)
}

// ===========================分割线===================================
func hello(w http.ResponseWriter, r *http.Request) {
	fmt.Println(r.Method)
	_, err := w.Write([]byte("hello"))
	if err != nil {
		panic(err)
	}
}

func main() {
	engine := NewEngine()
	engine.Any("/hello", hello)
	log.Fatal(engine.Run(":8080"))
}
```

## 0x04 分离路由&封装请求

```go
//分离路由
package frame

import "net/http"

/*
将用户请求路由拆出
*/

type router struct {
	handlers map[string]HandlerFunc
}

func newRouter() *router {
	return &router{handlers: make(map[string]HandlerFunc)}
}

func (r *router) addRoute(method, patten string, handler HandlerFunc) {
	key := method + "-" + patten
	r.handlers[key] = handler
}

func (r *router) handle(c *Context) {
	key := c.Method + "-" + c.Path
	if handler, ok := r.handlers[key]; ok {
		handler(c)
	} else {
		c.String(http.StatusNotFound, "404 NOT FOUND: %s\n", c.Path)
	}
}

//封装请求
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
	StatusCode int
}

func newContext(w http.ResponseWriter, r *http.Request) *Context {
	return &Context{
		Writer:  w,
		Request: r,
		Path:    r.URL.Path,
		Method:  r.Method,
	}
}

// PostForm 获取请求体参数
func (c *Context) PostForm(key string) string {
	return c.Request.FormValue(key)
}

// Query 获取查询参数
func (c *Context) Query(key string) string {
	return c.Request.URL.Query().Get(key)
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
func (c *Context) HTML(code int, html string) {
	c.SetHeader("Content-Type", "text/html")
	c.Status(code)
	_, err := c.Writer.Write([]byte(html))
	if err != nil {
		c.Error(500)
	}
}

// 调整框架
package frame

import (
"net/http"
)

// HandlerFunc 定义HandlerFunc用于设置用户请求约束 -设置为 func (*Context)
type HandlerFunc func(*Context)

type Engine struct {
	router *router
}

func NewEngine() *Engine {
	return &Engine{
		router: newRouter(),
	}
}
func (e *Engine) AddRoute(method, patten string, handler HandlerFunc) {
	e.router.addRoute(method, patten, handler)
}

// ServeHTTP 实现此方法即可将此解构丢入ListenAndServe
func (e *Engine) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// 构造请求-将请求封装到Context中
	c := newContext(w, r)
	// 执行请求
	e.router.handle(c)
}
```

## 0x05 前缀树路由

```go
package frame

import "strings"

/*
使用前缀树实现路由匹配
*/
type node struct {
	patten   string  // 匹配路由
	part     string  //匹配路由中的一部分
	children []*node // 子节点
	isWild   bool    //是否精确匹配 part中含有：或者*时为true
}

// matchChild
func (n *node) matchChild(part string) *node {
	for _, child := range n.children {
		if child.part == part || child.isWild {
			return child
		}
	}
	return nil
}

// matchChildren 匹配查找节点
func (n *node) matchChildren(part string) []*node {
	nodes := make([]*node, 0)
	for _, child := range n.children {
		if child.part == part || child.isWild {
			nodes = append(nodes, child)
		}
	}
	return nodes
}

// insert 递归插入节点 从顶层往下层 层层查找并插入
func (n *node) insert(patten string, parts []string, height int) {
	if len(parts) == height {
		n.patten = patten
		return
	}
	part := parts[height]
	child := n.matchChild(part)
	if child == nil {
		child = &node{part: part, isWild: part[0] == ':' || part[0] == '*'}
		n.children = append(n.children, child)
	}
	child.insert(patten, parts, height+1)
}

// search 递归查询节点
func (n *node) search(parts []string, height int) *node {
	if len(parts) == height || strings.HasPrefix(n.part, "*") {
		if n.patten == "" {
			return nil
		}
		return n
	}
	part := parts[height]
	children := n.matchChildren(part)
	for _, child := range children {
		result := child.search(parts, height+1)
		if result != nil {
			return result
		}
	}
	return nil
}

package frame

import (
"net/http"
"strings"
)

/*
将用户请求路由拆出
*/

type router struct {
	roots    map[string]*node
	handlers map[string]HandlerFunc
}

func newRouter() *router {
	return &router{
		roots:    make(map[string]*node),
		handlers: make(map[string]HandlerFunc),
	}
}

func parsePatten(patten string) []string {
	pattenSplit := strings.Split(patten, "/")

	parts := make([]string, 0)
	for _, item := range pattenSplit {
		if item != "" {
			parts = append(parts, item)
			// 当前匹配到*便不再往下匹配
			if item[0] == '*' {
				break
			}
		}
	}
	return parts
}

// addRoute 添加路由时 动态注册至前缀树结构中
func (r *router) addRoute(method, patten string, handler HandlerFunc) {
	parts := parsePatten(patten)
	key := method + "-" + patten

	_, ok := r.roots[method]
	if !ok {
		r.roots[method] = &node{}
	}

	r.roots[method].insert(patten, parts, 0)
	r.handlers[key] = handler
}

// getRoute 获取时，从前缀树结构中获取
func (r *router) getRoute(method, path string) (*node, map[string]string) {
	searchParts := parsePatten(path)
	params := make(map[string]string)
	root, ok := r.roots[method]
	if !ok {
		return nil, nil
	}
	n := root.search(searchParts, 0)
	if n != nil {
		parts := parsePatten(n.patten)
		for index, part := range parts {
			if part[0] == ':' {
				params[part[1:]] = searchParts[index]
			}
			if part[0] == '*' && len(part) > 1 {
				params[part[1:]] = strings.Join(searchParts[index:], "/")
				break
			}
		}
		return n, params
	}
	return nil, nil
}

func (r *router) handle(c *Context) {
	n, params := r.getRoute(c.Method, c.Path)
	if n != nil {
		c.Params = params
		key := c.Method + "-" + n.patten
		r.handlers[key](c)
	} else {
		c.String(http.StatusNotFound, "404 NOT FOUND: %s\n", c.Path)
	}
}

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
}

func newContext(w http.ResponseWriter, r *http.Request) *Context {
	return &Context{
		Writer:  w,
		Request: r,
		Path:    r.URL.Path,
		Method:  r.Method,
	}
}

} // Param 获取路径参数
func (c *Context) Param(key string) string {
	v, ok := c.Params[key]
	if ok {
		return v
	}
	return ""
}
```

## 0x06 路由分组

```go
package frame

import (
	"net/http"
)

// HandlerFunc 定义HandlerFunc用于设置用户请求约束 -设置为 func (*Context)
type HandlerFunc func(*Context)

// RouterGroup 路由分组
type RouterGroup struct {
	prefix     string
	middleware []HandlerFunc // 中间件支持
	parent     *RouterGroup  // 嵌套分组
	engine     *Engine       // 支持操作路由
}

func (r *RouterGroup) Group(prefix string) *RouterGroup {
	engine := r.engine
	newGroup := &RouterGroup{
		prefix: r.prefix + prefix,
		parent: r,
		engine: engine,
	}
	engine.groups = append(engine.groups, newGroup)
	return newGroup
}

func (r *RouterGroup) AddRoute(method, comp string, handler HandlerFunc) {
	patten := r.prefix + comp
	r.engine.router.addRoute(method, patten, handler)
}

func (r *RouterGroup) GET(patten string, handler HandlerFunc) {
	r.AddRoute("GET", patten, handler)
}

func (r *RouterGroup) POST(patten string, handler HandlerFunc) {
	r.AddRoute("POST", patten, handler)
}

func (r *RouterGroup) PUT(patten string, handler HandlerFunc) {
	r.AddRoute("PUT", patten, handler)
}

func (r *RouterGroup) DELETE(patten string, handler HandlerFunc) {
	r.AddRoute("DELETE", patten, handler)
}

func (r *RouterGroup) Any(patten string, handler HandlerFunc) {
	r.AddRoute("GET", patten, handler)
	r.AddRoute("POST", patten, handler)
	r.AddRoute("PUT", patten, handler)
	r.AddRoute("DELETE", patten, handler)
}

type Engine struct {
	*RouterGroup //当前engine可以使用路由组中的方法
	router       *router
	groups       []*RouterGroup // 存储所有分组
}

func NewEngine() *Engine {
	engine := &Engine{
		router: newRouter(),
	}
	engine.RouterGroup = &RouterGroup{engine: engine}
	engine.groups = []*RouterGroup{engine.RouterGroup}
	return engine
}
```

## 0x07 中间件

```go
// Use 实现中间件的添加
func (r *RouterGroup) Use(middlewares ...HandlerFunc) {
	r.middleware = append(r.middleware, middlewares...)
}

// ServeHTTP 实现此方法即可将此解构丢入ListenAndServe
func (e *Engine) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // 确认是否存在中间件
    var middlewares []HandlerFunc
    for _, rGroup := range e.groups {
    middlewares = append(middlewares, rGroup.middleware...)
    }
    // 构造请求-将请求封装到Context中
    c := newContext(w, r)
    // 将中间件封装至Context
    c.handlers = middlewares
    // 执行请求
    e.router.handle(c)
}

type Context struct {
    Writer     http.ResponseWriter
    Request    *http.Request
    Path       string
    Method     string
    Params     map[string]string // 获取路径参数
    StatusCode int
    
    handlers []HandlerFunc // 保存中间件 方便中间件的后续调用
    index    int
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

func (r *router) handle(c *Context) {
    n, params := r.getRoute(c.Method, c.Path)
    /*
        将中间封装至请求中，通过Next来启动
    */
    if n != nil {
    c.Params = params // 将参数封装至Context
    key := c.Method + "-" + n.patten
    c.handlers = append(c.handlers, r.handlers[key])
    //r.handlers[key](c) 这段直接被放在中间件之后，中间件通过Next启动后，会主动将Context传递至Handler中
    } else {
    c.handlers = append(c.handlers, func(c *Context) {
    c.String(http.StatusNotFound, "404 NOT FOUND: %s\n", c.Path)
    })
    }
    
    // 向下处理
    c.Next()
}
```

## 0x08 静态文件&模板渲染

```go
package frame

import (
	"html/template"
	"net/http"
	"path"
)

// HandlerFunc 定义HandlerFunc用于设置用户请求约束 -设置为 func (*Context)
type HandlerFunc func(*Context)

// RouterGroup 路由分组
type RouterGroup struct {
	prefix     string
	middleware []HandlerFunc // 中间件支持
	parent     *RouterGroup  // 嵌套分组
	engine     *Engine       // 支持操作路由
}

func (r *RouterGroup) Group(prefix string) *RouterGroup {
	engine := r.engine
	newGroup := &RouterGroup{
		prefix: r.prefix + prefix,
		parent: r,
		engine: engine,
	}
	engine.groups = append(engine.groups, newGroup)
	return newGroup
}

// createStaticHandler 借用http FileHandler对静态文件进行处理
func (r *RouterGroup) createStaticHandler(relativePath string, fs http.FileSystem) HandlerFunc {
	absolutePath := path.Join(r.prefix, relativePath)
	fileServer := http.StripPrefix(absolutePath, http.FileServer(fs))
	return func(c *Context) {
		file := c.Param("filename")
		if _, err := fs.Open(file); err != nil {
			c.Status(404)
			return
		}
		fileServer.ServeHTTP(c.Writer, c.Request)
	}
}

// Use 实现中间件的添加
func (r *RouterGroup) Use(middlewares ...HandlerFunc) {
	r.middleware = append(r.middleware, middlewares...)
}

// Static 处理静态文件
func (r *RouterGroup) Static(relativePath, root string) {
	// 构造文件处理器
	handler := r.createStaticHandler(relativePath, http.Dir(root))

	// 构造请求路径，*匹配文件
	urlPatten := path.Join(relativePath, "/*filename")
	r.GET(urlPatten, handler)
}


type Engine struct {
	*RouterGroup  //当前engine可以使用路由组中的方法
	router        *router
	groups        []*RouterGroup     // 存储所有分组
	htmlTemplates *template.Template // 添加HTML template支持
	funcMap       template.FuncMap   // 添加HTML funcMap
}

func NewEngine() *Engine {
	engine := &Engine{
		router: newRouter(),
	}
	engine.RouterGroup = &RouterGroup{engine: engine}
	engine.groups = []*RouterGroup{engine.RouterGroup}
	return engine
}

func (e *Engine) SetFuncMap(funcMap template.FuncMap) {
	e.funcMap = funcMap
}

// LoadHTMLGlob 加载静态文件并使用funcMap渲染
func (e *Engine) LoadHTMLGlob(patten string) {
	e.htmlTemplates = template.Must(template.New("").Funcs(e.funcMap).ParseGlob(patten))
}

// ServeHTTP 实现此方法即可将此解构丢入ListenAndServe
func (e *Engine) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// 确认是否存在中间件
	var middlewares []HandlerFunc
	for _, rGroup := range e.groups {
		middlewares = append(middlewares, rGroup.middleware...)
	}
	// 构造请求-将请求封装到Context中
	c := newContext(w, r)
	// 将中间件封装至Context
	c.handlers = middlewares
	// 将engine封装至Context
	c.engine = e
	// 执行请求
	e.router.handle(c)
}

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

// HTML 相应HTML
func (c *Context) HTML(code int, name string, data interface{}) {
	c.SetHeader("Content-Type", "text/html")
	c.Status(code)
	err := c.engine.htmlTemplates.ExecuteTemplate(c.Writer, name, data)
	if err != nil {
		c.Error(500)
	}
}
```

## 0x09 错误恢复

```go
package frame

import (
	"fmt"
	"log"
	"runtime"
	"strings"
)

func trace(err string) string {
	var pcs [32]uintptr
	n := runtime.Callers(3, pcs[:]) // skip first 3 caller
	var str strings.Builder
	str.WriteString(err + "\nTraceback:")
	for _, pc := range pcs[:n] {
		fn := runtime.FuncForPC(pc)
		file, line := fn.FileLine(pc)
		str.WriteString(fmt.Sprintf("\n\t%s:%d", file, line))
	}
	return str.String()
}

// Recovery 捕获异常
func Recovery() HandlerFunc {
	return func(c *Context) {
		defer func() {
			if err := recover(); err != nil {
				msg := trace(fmt.Sprintf("%s", err))
				log.Printf("%s\n\n", msg)
			}
		}()
		c.Next()
	}
}
```
