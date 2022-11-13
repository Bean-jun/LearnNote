/*
结构体绑定方法

注意点：
 1. 结构体必须和自己对应的方法封装在一个包当中哦
 2. 由于数组和结构体都是值类型，故在处理的时候尤为小心
    下面的setAge的两个方法就是很好的例子
*/
package main

import "fmt"

// 定义学生结构体
// 结构体中，首字母小写名称及字段将具备模块私有行，避免方式请将对应内容首字母大写
type Student struct {
	Id   int
	Name string
	Age  int
	Sex  bool
}

//给结构体绑定方法
func (self Student) getName() string {
	// (self Student) 声明这个函数是结构体绑定的方法， self是Student结构体的对象
	return self.Name
}

// 修改结构体的值需要注意，由于结构体传递默认是传值， 很容易出错，请看下面两个绑定的方法
func (self Student) setAge(age int) {
	// 这种值传递方式其实是修改不了的
	self.Age = age
}
func (self *Student) setAge2(age int) {
	// 通过指针来处理可以修改成功
	self.Age = age
	// 上述写法原则上应该是
	// (*self).Age = age
	// 由于go语言的语法糖可以不需要写这么复杂
}

func main() {
	s1 := Student{1, "小红", 10, true}
	fmt.Printf("当前人物的姓名为：%s\n", s1.getName())

	fmt.Printf("修改前，当前人物的年龄为：%d\n", s1.Age)
	s1.setAge(100) // 等价于写法 Student.setAge(s1, 100)
	fmt.Printf("改法1， 当前人物的年龄为：%d\n", s1.Age)
	s1.setAge2(100) // 等价于写法 (&s1).setAge2(100)
	fmt.Printf("改法2， 当前人物的年龄为：%d\n", s1.Age)
}
