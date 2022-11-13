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
