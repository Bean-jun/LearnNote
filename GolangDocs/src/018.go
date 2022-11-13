package main

func Add(n ...int) (m int) {
	for _, v := range n {
		m += v
	}
	return
}
