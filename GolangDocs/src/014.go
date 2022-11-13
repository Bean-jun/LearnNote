/*
结构体的嵌套-实现对象的继承效果
*/
package main

import "fmt"

type Teacher struct {
	Name  string
	Age   int
	Title string
}

func (self Teacher) teacherInfo() {
	fmt.Printf("老师的姓名:%s, 年龄是：%d, 职称是：%s\n", self.Name, self.Age, self.Title)
}

type Course struct {
	Teacher Teacher
	Name    string
	Time    string
}

func (self Course) courceInfo() {
	// 调用老师的方法
	self.Teacher.teacherInfo()
	fmt.Printf("课程信息：%s, 上课时间：%s, 主讲人：%s\n", self.Name, self.Time, self.Teacher.Name)
}

func main() {
	c1 := Course{
		Teacher: Teacher{
			Name:  "小王",
			Age:   20,
			Title: "Python讲师",
		},
		Name: "Python程序设计",
		Time: "2021-8-29",
	}

	c1.Teacher.teacherInfo()

	c1.courceInfo()
}
