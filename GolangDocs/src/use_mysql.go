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
