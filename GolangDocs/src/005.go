package main

import "fmt"

/*
字符串的一些小问题
*/
func main() {
	content := "name:杰瑞"
	fmt.Println("当前内容为", content)
	fmt.Println(content[0], content[5], "得到的是对应Unicode的值")
	fmt.Printf("0号位置为%c, 5号位置为%c\n", content[0], content[5])
	fmt.Println("当前内容长度为", len(content), "实际长度为7,原因是中文使用Unicode编码，使用三个字节，而len函数就是获取的字节数量")
	fmt.Println("破解方案：将每一个内容放进数组，求数组的长度即可")
	// 将其转换为数组即可解决问题，这里的rune就是一个int32的类型【准确来说是slice】
	newContent := []rune(content)
	fmt.Println(newContent)
	fmt.Printf("0号位置为%c, 5号位置为%c\n", newContent[0], newContent[5])
	fmt.Println("当前内容长度为", len(newContent))
}
