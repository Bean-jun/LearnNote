package db

import (
	"reflect"
	"testing"

	_ "github.com/go-sql-driver/mysql"
)

func TestInsertData(t *testing.T) {
	tests := []struct {
		name string
	}{
		{"张三"}, {"李四"}, {"王五"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			InsertData(tt.name)
		})
	}
}

func Test_query(t *testing.T) {
	tests := []struct {
		name    string
		want    []User
		wantErr bool
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := query()
			if (err != nil) != tt.wantErr {
				t.Errorf("query() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !reflect.DeepEqual(got, tt.want) {
				t.Errorf("query() = %v, want %v", got, tt.want)
			}
		})
	}
}
func Test_update(t *testing.T) {
	type args struct {
		username string
		id       int
	}
	tests := []struct {
		name string
		args args
	}{
		{"li01", args{"li01", 3}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			update(tt.args.username, tt.args.id)
		})
	}
}

func Test_delete(t *testing.T) {
	type args struct {
		id int
	}
	tests := []struct {
		name string
		args args
	}{
		{"001", args{3}},
		{"002", args{4}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			delete(tt.args.id)
		})
	}
}

func Test_insertTx(t *testing.T) {
	type args struct {
		username string
	}
	tests := []struct {
		name string
		args args
	}{
		// TODO: Add test cases.
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			insertTx(tt.args.username)
		})
	}
}

func Test_prepareInsertDemo(t *testing.T) {
	type args struct {
		usernames []string
	}
	tests := []struct {
		name string
		args args
	}{
		{"001", args{[]string{"bean001", "bean002"}}},
		{"002", args{[]string{"bean003", "bean004"}}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			prepareInsertDemo(tt.args.usernames...)
		})
	}
}
