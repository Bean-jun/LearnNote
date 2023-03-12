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
	*RouterGroup  //当前engine可以使用路由组中的方法
	router        *router
	groups        []*RouterGroup     // 存储所有分组,用于处理当前分组上的中间件
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

func (e *Engine) AddRoute(method, patten string, handler HandlerFunc) {
	e.router.addRoute(method, patten, handler)
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

// Run 用户调用Run实现server启动
func (e *Engine) Run(addr string) error {
	return http.ListenAndServe(addr, e)
}
