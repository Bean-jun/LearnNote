package main

import (
	"fmt"
)

func main() {
	var score int
	fmt.Println("请输入数字:")
	fmt.Scan(&score)
	fmt.Println("当前的值为：", score)

	if score >= 90 {
		fmt.Println("A")
	} else if score >= 80 {
		fmt.Println("B")
	} else if score >= 70 {
		fmt.Println("C")
	} else if score >= 60 {
		fmt.Println("D")
	} else {
		fmt.Println("E")
	}
}
