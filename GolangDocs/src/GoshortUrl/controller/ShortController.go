package controller

import (
	"github.com/Bean-jun/shortUrl/pkg"
	"net/http"
)

// ShortController 短连接生成器
func ShortController(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "POST":
		longUrl := r.FormValue("url")
		if longUrl == "" {
			pkg.ToResponse(w, "连接不可以为空")
			return
		}

		keys := pkg.Generate()
		pkg.Set(keys, longUrl)
		pkg.ToResponse(w, pkg.AddPrefix(keys))
		return
	default:
		w.WriteHeader(http.StatusBadRequest)
	}
}
