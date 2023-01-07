sitemap:
	tree --dirsfirst -L 2 > sitemap.txt

preview: sitemap
	python3 -m http.server