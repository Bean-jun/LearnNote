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
