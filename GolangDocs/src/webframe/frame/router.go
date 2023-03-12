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
