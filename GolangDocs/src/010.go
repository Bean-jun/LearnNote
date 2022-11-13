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
