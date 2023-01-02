1. 术语解释：

    ```shell
    占位符问题：
    补充：不同的数据库中，SQL语句使用的占位符语法不尽相同。
        数据库	占位符语法
        MySQL	?
        PostgreSQL	$1, $2等
        SQLite	? 和$1
        Oracle	:name

    什么是预处理？
        普通SQL语句执行过程：

            客户端对SQL语句进行占位符替换得到完整的SQL语句。
            客户端发送完整SQL语句到MySQL服务端
            MySQL服务端执行完整的SQL语句并将结果返回给客户端。
        预处理执行过程：

            把SQL语句分成两部分，命令部分与数据部分。
            先把命令部分发送给MySQL服务端，MySQL服务端进行SQL预处理。
            然后把数据部分发送给MySQL服务端，MySQL服务端对SQL语句进行占位符替换。
            MySQL服务端执行完整的SQL语句并将结果返回给客户端。

    为什么要预处理？
        优化MySQL服务器重复执行SQL的方法，可以提升服务器性能，提前让服务器编译，一次编译多次执行，节省后续编译的成本。
        避免SQL注入问题。
    ```

2. 操作代码

```go
// GolangDocs/src/use_mysql.go
package db

/*
操作mysql
CREATE TABLE `user` (
    `user_id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) DEFAULT NULL,
    `sex` varchar(255) DEFAULT NULL,
    `email` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`user_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
*/
import (
	"database/sql"
	"errors"
	"fmt"
	"log"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var DB *sql.DB

func init() {
	// 函数初始化
	db, err := sql.Open("mysql", "root:0009@tcp(localhost:3306)/golang_base?charset=utf8&parseTime=True")
	if err != nil {
		panic(err)
	}
	// 最大空闲链接数，默认不配置是2个最大空闲连接数
	db.SetMaxIdleConns(5)
	// 最大连接数，默认不配置，是不限制最大连接数
	db.SetMaxOpenConns(100)
	// 空闲链接最大存活时间
	db.SetConnMaxIdleTime(time.Minute * 3)
	// 连接最大存活时间
	db.SetConnMaxLifetime(time.Minute * 3)
	err = db.Ping()
	if err != nil {
		db.Close()
		panic(err)
	}
	DB = db
}

type User struct {
	UserId   int    `db:"user_id"`
	Username string `db:"username"`
	Sex      string `db:"sex"`
	Email    string `db:"email"`
}

// InsertData 数据插入
func InsertData(username string) {
	r, err := DB.Exec("INSERT INTO user (username,sex,email) VALUES(?,?,?)", username, "man", "张三@bean.com")
	if err != nil {
		panic(err)
	}
	id, err := r.LastInsertId()
	if err != nil {
		panic(err)
	}
	fmt.Println("insert success :", id)
}

// query 数据查询多条
func query() ([]User, error) {
	rows, err := DB.Query("select * from user")
	if err != nil {
		log.Println("查询出现错误:", err)
		return nil, errors.New(err.Error())
	}
	ret := []User{}
	user := User{}

	defer rows.Close()
	for rows.Next() {
		if err := rows.Scan(&user.UserId, &user.Username, &user.Sex, &user.Email); err != nil {
			log.Println("scan error:", err)
			return nil, errors.New(err.Error())
		}
		ret = append(ret, user)
	}
	return ret, nil
}

// update update数据
func update(username string, id int) {
	ret, err := DB.Exec("update user set username=? where user_id=?", username, id)
	if err != nil {
		log.Println("更新出现问题:", err)
		return
	}
	affected, _ := ret.RowsAffected()
	fmt.Println("更新成功的行数:", affected)
}

// delete
func delete(id int) {
	ret, err := DB.Exec("delete from user where user_id=?", id)
	if err != nil {
		log.Println("删除出现问题:", err)
		return
	}
	affected, _ := ret.RowsAffected()
	fmt.Println("删除成功的行数:", affected)
}

// golang数据库预处理`func (db *DB) Prepare(query string) (*Stmt, error)`
// 预处理插入示例 crud基本一致
func prepareInsertDemo(usernames ...string) {
	sqlStr := "INSERT INTO user (username,sex,email) VALUES(?,?,?)"
	stmt, err := DB.Prepare(sqlStr)
	if err != nil {
		panic(err)
	}
	defer stmt.Close()
	for _, username := range usernames {
		_, err = stmt.Exec(username, "man", "张三@bean.com")
		if err != nil {
			panic(err)
		}
	}
	fmt.Println("insert success.")
}

// go操作mysql事务
func insertTx(username string) {
	tx, err := DB.Begin()
	if err != nil {
		log.Println("开启事务错误:", err)
		return
	}
	ret, err := tx.Exec("insert into user (username,sex,email) values (?,?,?)", username, "man", "test@bean.com")
	if err != nil {
		log.Println("事务sql执行出错:", err)
		return
	}
	id, _ := ret.LastInsertId()
	fmt.Println("插入成功:", id)
	if username == "lisi" {
		fmt.Println("回滚...")
		_ = tx.Rollback()
	} else {
		_ = tx.Commit()
	}
}
```

```go
// GolangDocs/src/use_mysql_test.go
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
```