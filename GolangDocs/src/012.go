package main

import "fmt"

func main() {
	// 异常处理逻辑
	defer func() {
		err := recover()
		fmt.Println("我是异常：", err)
		fmt.Println("后面的逻辑还是要执行的~")
	}()

	fmt.Println("很正常的执行代码中~")
	fmt.Println("我还是处理问题中~")
	panic("糟糕啦，我开始异常了~")
}
