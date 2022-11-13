package main

import "fmt"

func Swap(a, b *int) {
	var c int
	c = *a
	*a = *b
	*b = c
}

func main() {
	// 交换变量值
	num1 := 100
	num2 := 200
	num1, num2 = num2, num1
	fmt.Println("交换之后的结果为：", num1, num2)
	// 使用函数处理
	Swap(&num1, &num2)
	fmt.Println("交换之后的结果为：", num1, num2)
}
