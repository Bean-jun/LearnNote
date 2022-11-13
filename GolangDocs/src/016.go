/*
接口和接口之间也可以继承
*/

package main

import "fmt"

type Payment interface {
	Pay() string
}
type BoyFirend interface {
	// 直接继承Payment接口，下面的结构体想要使用，必须实现所有的方法
	Payment
	Show() string
}

// 对于BoyFirend这个接口必须实现Pay()及Show()两个方法
type People struct {
	Name string
	Age  int
}

func (self People) Pay() string {
	return self.Name + "花费了xx元..."
}

// 若是仅仅实现Pay()方法，而没实现Show方法就没有办法直接使用BoyFirend接口
func (self People) Show() string {
	return self.Name + "长的还不错..."
}

func main() {
	// 创建一个对象
	var p1 Payment = People{"张三", 20}
	fmt.Println(p1.Pay())

	var p2 BoyFirend = People{"李四", 23}
	fmt.Println(p2.Pay())
	fmt.Println(p2.Show())
}
