package controller

import (
	"github.com/Bean-jun/shortUrl/pkg"
	"html/template"
	"net/http"
)

// IndexController 首页控制器
func IndexController(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		shortUrl := r.URL.Query().Get("url")
		if shortUrl == "" {
			t, err := template.ParseFiles("templates/index.tml")
			if err != nil {
				panic(err)
			}
			err = t.Execute(w, map[string]string{
				"name": "短连接生成器",
			})
			if err != nil {
				return
			}
			return
		}
		value := pkg.Get(shortUrl)
		w.Header().Set("Location", value)
		w.WriteHeader(http.StatusMovedPermanently)
		return
	default:
		w.WriteHeader(http.StatusBadRequest)
	}
}
