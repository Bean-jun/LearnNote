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
