package main

import "fmt"

func main() {
	// 创建map
	// 1.
	m1 := make(map[string]int)
	m1["小明"] = 100
	m1["小红"] = 120
	m1["小白"] = 110
	m1["小黑"] = 121
	fmt.Printf("%v, %T\n", m1, m1)
	// 2.
	m2 := map[string]int{
		"a": 1,
		"b": 2,
	}
	fmt.Println(m2)

	// 删除键
	delete(m1, "小明")
	fmt.Printf("%v, %T\n", m1, m1)
	// 不存在的键删除,不会报错
	delete(m1, "老王")

	// 修改键
	m1["小白"] = 10

	// 遍历
	for index, data := range m1 {
		fmt.Println(index, data)
	}
}
