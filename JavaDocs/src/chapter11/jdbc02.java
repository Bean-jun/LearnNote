package chapter11;

import java.sql.*;

public class jdbc02 {

    // 创建数据库
    public static void createDB(Statement stat, String db) throws SQLException {
        stat.execute("create database if not exists jdbcdemo charset=utf8");
        System.out.println(stat.getUpdateCount());
    }

    // 创建表
    public static void createTable(Statement stat, String tableSQL) throws SQLException {
        stat.execute(tableSQL);
        System.out.println(stat.getUpdateCount());
    }

    // 插入数据
    public static void InsertTable(Statement stat, String SQL) throws SQLException {
        stat.execute(SQL);
        System.out.println(stat.getUpdateCount());
    }

    // 批量插入数据
    public static void InsertBatchTable(Statement stat, String[] SQL) throws SQLException {
        for (String _SQL : SQL) {
            stat.addBatch(_SQL);
        }
        stat.executeBatch();
    }

    public static void main(String[] args) throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcdemo", "root", "0009");
        Statement stat = conn.createStatement();

        // 创建数据表
        // createDB(stat, "jdbcdemo");
        
        // 创建表
        createTable(stat, """
                    create table if not exists users(
                        id int primary key auto_increment,
                        username varchar(50) not null,
                        age int,
                        sex varchar(20)
                    );
                """);
        
        // 插入数据
        InsertTable(stat, "insert into users(`username`, `age`, `sex`) values (\"tom\", 12, \"男\")");
        InsertTable(stat, "insert into users(`username`, `age`, `sex`) values (\"alex\", 13, \"男\")");
        InsertTable(stat, "insert into users(`username`, `age`, `sex`) values (\"jerry\", 14, \"女\")");

        // 批量插入数据
        InsertBatchTable(stat, new String[]{
            "insert into users(`username`, `age`, `sex`) values (\"tom\", 1, \"男\")",
            "insert into users(`username`, `age`, `sex`) values (\"tom\", 2, \"男\")",
            "insert into users(`username`, `age`, `sex`) values (\"tom\", 3, \"男\")",
            "insert into users(`username`, `age`, `sex`) values (\"tom\", 4, \"男\")",
            "insert into users(`username`, `age`, `sex`) values (\"tom\", 5, \"男\")",
        });
        stat.close();
        conn.close();
    }
}
