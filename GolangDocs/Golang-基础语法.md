### 1. 查看go版本

```shell
go version
```

### 2. 第一个hello world

```go
// GolangDocs/src/001.go
package main

import "fmt"

func main() {
	fmt.Println("Hello Go~")
}
```

### 3. if语句

```go
// GolangDocs/src/002.go
package main

import (
	"fmt"
)

func main() {
	var score int
	fmt.Println("请输入数字:")
	fmt.Scan(&score)
	fmt.Println("当前的值为：", score)

	if score >= 90 {
		fmt.Println("A")
	} else if score >= 80 {
		fmt.Println("B")
	} else if score >= 70 {
		fmt.Println("C")
	} else if score >= 60 {
		fmt.Println("D")
	} else {
		fmt.Println("E")
	}
}
```

### 4. for语句

```go
// GolangDocs/src/003.go
package main

import "fmt"

func main() {
	//基本for循环写法
	for i := 0; i <= 3; i++ {
		fmt.Println(i)
	}

	// for循环配合range实现对字符串的访问
	msg := "name is Tom"
	for index, data := range msg {
		fmt.Printf("%v 当前值%c\n", index, data)
	}
}
```

### 5. switch语句

```go
// GolangDocs/src/004.go
package main

import "fmt"

func main() {
	score := 100

	switch score {
	case 100:
		fmt.Println("100分，很优秀")
	case 90:
		fmt.Println("90分,也很不错")
	case 80:
		fmt.Println("80分，还可以")
	}
}
```

### 6. 字符串常见陷阱

```go
// GolangDocs/src/005.go
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
```

### 7. 数组

```go
// GolangDocs/src/006.go
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
```

### 8. slice

```go
// GolangDocs/src/007.go
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
```

### 9. map

```go
// GolangDocs/src/008.go
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
```

### 10. point

```go
// GolangDocs/src/009.go
package main

import "fmt"

func Swap(a, b *int) {
	var c int
	c = *a
	*a = *b
	*b = c
}

func main() {
	// 交换变量值
	num1 := 100
	num2 := 200
	num1, num2 = num2, num1
	fmt.Println("交换之后的结果为：", num1, num2)
	// 使用函数处理
	Swap(&num1, &num2)
	fmt.Println("交换之后的结果为：", num1, num2)
}
```

### 11. 函数

```go
// GolangDocs/src/010.go
package main

import (
	"errors"
	"fmt"
)

func Add(params ...int) (res int, err error) {
	for _, data := range params {
		res += data
	}

	if res > 100 {
		err = errors.New("大于100咯")
	}
	return res, err
}

func main() {
	array1 := [10]int{100, 10, 10, 10, 10, 10, 10, 9}
	slice := array1[:10]
	res, err := Add(slice...)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(res)
	}
}
```

### 12. defer

```go
// GolangDocs/src/011.go
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
```

### 13. panic

```go
// GolangDocs/src/012.go
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
```

### 14. struct

```go
// GolangDocs/src/013.go
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
```

```go
// GolangDocs/src/014.go
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
```

### 15. interface

```go
// GolangDocs/src/015.go
/*
interface学习
*/

package main

import "fmt"

// 定义接口
// Pay()表示内部需要实现的方法, string表示该方法的返回值
type Payment interface {
	Pay() string
	Call() string
}

// 定义支付宝支付结构体
type AliPay struct {
	orderId        string
	createDatetime string
}

// 实现AliPay的支付方法，这里和接口保持一致就可以利用到接口了
func (self AliPay) Pay() string {
	msg := self.createDatetime + "-订单:" + self.orderId + "支付成功"
	return msg
}

// 必须将Payment的Call方法实现才可以实现`Payment = AliPay{"0000001", "2021-8-30"}`这样的调用
func (self AliPay) Call() string {
	msg := self.orderId + "支付成功"
	return msg
}

func main() {
	// 处理用户订单
	// 需要实现继承关系，更多的需要实现接口的方法
	var userPay_1 Payment = AliPay{"0000001", "2021-8-30"}
	fmt.Println(userPay_1.Pay())
	fmt.Println(userPay_1.Call())
}
```

```go
// GolangDocs/src/016.go
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
```

```go
// GolangDocs/src/017.go
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
```

### 16. testing

- `go test`进行测试
- `go test -v`查看测试verbose详细
- `go test -cover`覆盖率测试
- `go test -cover -coverprofile=c.out`将测试结果输出到`c.out`
- `go tool cover -html=c.out`以HTML方式查看`c.out`测试用例结果

```go
// GolangDocs/src/018.go
package main

func Add(n ...int) (m int) {
	for _, v := range n {
		m += v
	}
	return
}
```

```go
// GolangDocs/src/019.go
package main

import "testing"

func TestAdd(t *testing.T) {
	type args struct {
		n []int
	}
	tests := []struct {
		name string
		args
		wantM int
	}{
		// TODO: Add test cases.
		{
			name:  "t01",
			args:  args{[]int{1, 2, 3}},
			wantM: 6,
		},
		{
			name:  "t02",
			args:  args{[]int{2, 3, 4}},
			wantM: 9,
		},
		{
			name:  "t03",
			args:  args{[]int{2, 3, 4, 1}},
			wantM: 10,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotM := Add(tt.args.n...); gotM != tt.wantM {
				t.Errorf("Add() = %v, want %v", gotM, tt.wantM)
			}
		})
	}
}
```

```go
// GolangDocs/src/020.go
package main

import "testing"

func BenchmarkAdd2(b *testing.B) {
	for i := 0; i <= b.N; i++ {
		Add2([]int{1, 2, 3}...)
	}
}
```
