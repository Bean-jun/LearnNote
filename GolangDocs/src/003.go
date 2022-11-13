package main

import "fmt"

func main() {
	//基本for循环写法
	for i := 0; i <= 3; i++ {
		fmt.Println(i)
	}

	// for循环配合range实现对字符串的访问
	msg := "name is Tom"
	for index, data := range msg {
		fmt.Printf("%v 当前值%c\n", index, data)
	}
}
