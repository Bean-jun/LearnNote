package main

import (
	"github.com/Bean-jun/shortUrl/controller"
	"github.com/Bean-jun/shortUrl/pkg"
	"log"
	"net/http"
	"time"
)

func main() {
	http.HandleFunc("/", controller.IndexController)
	http.HandleFunc("/short", controller.ShortController)
	log.Printf("start serve in %s://%s%s\n", pkg.Schema, pkg.Host, pkg.Port)
	if pkg.ShowUrl {
		go func() {
			for {
				log.Println(pkg.Url.UrlMap)
				time.Sleep(time.Second * 3)
			}
		}()
	}
	err := http.ListenAndServe(pkg.Port, nil)
	if err != nil {
		log.Println(err)
	}
}
