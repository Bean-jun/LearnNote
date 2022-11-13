package main

import "testing"

func BenchmarkAdd2(b *testing.B) {
	for i := 0; i <= b.N; i++ {
		Add2([]int{1, 2, 3}...)
	}
}
