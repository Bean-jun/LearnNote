package main

import "fmt"

func main() {
	//创建一个slice
	// 1.
	s1 := []int{}
	fmt.Printf("content:%v, type:%T\n", s1, s1)
	// 2.
	var s2 []string
	fmt.Printf("content:%v, type:%T\n", s2, s2)
	// 3.
	s3 := []int{1, 2, 3}
	fmt.Printf("content:%v, type:%T\n", s3, s3)
	// 4.
	var s4 []int = []int{1, 2, 3, 44}
	fmt.Printf("content:%v, type:%T\n", s4, s4)
	// 5. 使用make创建slice
	s5 := make([]int, 4)
	fmt.Printf("content:%v, type:%T\n", s5, s5)
	s6 := [6]int{123, 12, 14, 56, 8}
	fmt.Printf("content:%v, type:%T\n", s6, s6)
	// 6. 直接将数组切片亦可
	s7 := s6[3:4]
	fmt.Printf("content:%v, type:%T\n", s7, s7)
	// slice由值，长度及空间大小组合而成,空间大小是动态变化的，因为slice底层就是数组实现的
	fmt.Printf("s7的长度为:%d, 空间大小为:%d\n", len(s7), cap(s7))
}
