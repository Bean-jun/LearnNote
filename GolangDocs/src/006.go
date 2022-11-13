/*
数组的创建方式
*/
package main

import "fmt"

func main() {
	//方式一 创建数组
	var array3 [5]int
	fmt.Println(array3)

	//方式二 创建数组并初始化
	var array1 = [5]int{12, 1, 12, 1, 99}
	fmt.Println(array1)

	// 创建数组并初始化
	var array4 [3]int = [3]int{1, 11, 2}
	fmt.Println(array4)

	//方式三 创建数组并初始化
	array2 := [5]string{"abc", "bcd", "a", "sf", "12"}
	fmt.Println(array2)

	//自动初始化长度
	array5 := [...]int{12, 11, 1}
	fmt.Println(array5)
}
