/*
空接口
*/

package main

import "fmt"

// 空接口
type EmptyInterface interface {
}

// 定义一个接受任意类型的函数
func run(i interface{}) {
	fmt.Println(i)
}

// 传入参数类型的断言
func assertTest(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Println("这是一个整数", v)
	case string:
		fmt.Println("这是一个字符串", v)
	}
}

func main() {
	var abc EmptyInterface
	abc = 100
	fmt.Println(abc)
	abc = "100"
	fmt.Println(abc)

	// 空接口可以承接任何类型的数据,当然空接口可以简写
	var bcd interface{}
	bcd = 101
	fmt.Println(bcd)
	bcd = "102"
	fmt.Println(bcd)

	// 参数传递将可以创建任意类型的数据,其中最好的例子就是`fmt.Println()`

	// 定义一个这样的函数试试看哦
	run("asfasdfa")
	run(101231230)

	// 传入参数类型的断言
	assertTest(10)
	assertTest("adfasd")
}
