package frame

import (
	"fmt"
	"reflect"
	"testing"
)

func newTestRouter() *router {
	r := newRouter()
	r.addRoute("GET", "/", nil)
	r.addRoute("GET", "/hello/:name", nil)
	r.addRoute("GET", "/hello/b/c", nil)
	r.addRoute("GET", "/hi/:name", nil)
	r.addRoute("GET", "/assets/*filepath", nil)
	return r
}

func TestParsePattern(t *testing.T) {
	ok := reflect.DeepEqual(parsePatten("/p/:name"), []string{"p", ":name"})
	ok = ok && reflect.DeepEqual(parsePatten("/p/*"), []string{"p", "*"})
	ok = ok && reflect.DeepEqual(parsePatten("/p/*name/*"), []string{"p", "*name"})
	if !ok {
		t.Fatal("test parsePatten failed")
	}
}

func TestGetRoute(t *testing.T) {
	r := newTestRouter()
	n, ps := r.getRoute("GET", "/hello/hello")

	if n == nil {
		t.Fatal("nil shouldn't be returned")
	}

	if n.patten != "/hello/:name" {
		t.Fatal("should match /hello/:name")
	}

	if ps["name"] != "hello" {
		t.Fatal("name should be equal to 'hello'")
	}

	fmt.Printf("matched path: %s, params['name']: %s\n", n.patten, ps["name"])

}
