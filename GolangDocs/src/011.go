package main

import "fmt"

func main() {
	a := 10
	b := 100
	c := 1000

	defer func(args int, args2 *int) {
		// 使用到闭包概念，故结果为11
		fmt.Println("a的值为：", a)
		// 直接传递值的操作,故结果为100
		fmt.Println("b的值为：", args)
		// 通过指针来处理，结果为1001
		fmt.Println("c的值为：", *args2)
	}(b, &c)

	a++
	b++
	c++
	fmt.Println("我完事了~")
}
