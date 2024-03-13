1. 连接数据库

    ```java
    package chapter11;

    import java.sql.*;

    public class jdbc01 {
        public static void main(String[] args) throws SQLException {
                // 1. 创建连接
                Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306", "root", "root");
                // 2. 创建执行SQL的Statement对象
                Statement stat = conn.createStatement();
                // 3. 执行查询结果
                ResultSet set = stat.executeQuery("select now()");
                // 4. 查看结果
                while (set.next()){
                    System.out.println(set.getString(1));
                }
                // 5. 关闭
                stat.close();
                conn.close();
        }
    }
    ```

2. 使用jdbc对数据库执行些许SQL

    ```java
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
            Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcdemo", "root", "root");
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
    ```

3. 使用jdbc查询结果映射为对象

    ```java
    package chapter11;

    import java.sql.*;

    class User {
        private int id;
        private String username;
        private int age;
        private String sex;

        public User(int id, String username, int age, String sex) {
            this.id = id;
            this.username = username;
            this.age = age;
            this.sex = sex;
        }

        @Override
        public String toString() {
            return "User [id=" + id + ", username=" + username + ", age=" + age + ", sex=" + sex + "]";
        }
    }

    public class jdbc03 {
        public static void main(String[] args) throws SQLException {
            Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcdemo", "root", "root");
            Statement stat = conn.createStatement();

            ResultSet set = stat.executeQuery("select * from users");
            while (set.next()) {
                User u = new User(set.getInt(1), set.getString(2), set.getInt(3), set.getString(4));
                System.out.println(u);
            }

            stat.close();
            conn.close();
        }
    }
    ```

4. 使用prepareStatement实现预编译参数插入

    ```java
    package chapter11;

    import java.sql.*;

    class User {
        private int id;
        private String username;
        private int age;
        private String sex;

        public User(int id, String username, int age, String sex) {
            this.id = id;
            this.username = username;
            this.age = age;
            this.sex = sex;
        }

        @Override
        public String toString() {
            return "User [id=" + id + ", username=" + username + ", age=" + age + ", sex=" + sex + "]";
        }
    }

    public class jdbc04 {
        public static void main(String[] args) throws SQLException {
            Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcdemo", "root", "0009");
            PreparedStatement stat = conn.prepareStatement("select * from users where id=?;");

            // 在第一个参数位置  设置值为4
            System.out.println(stat.toString());
            stat.setInt(1, 4);
            System.out.println(stat.toString());

            ResultSet set = stat.executeQuery();
            while (set.next()) {
                User u = new User(set.getInt(1), set.getString(2), set.getInt(3), set.getString(4));
                System.out.println(u);
            }

            stat.close();
            conn.close();
        }
    }
    ```

5. jdbc事务

    ```java
    package chapter11;

    import java.sql.Connection;
    import java.sql.DriverManager;
    import java.sql.PreparedStatement;
    import java.sql.ResultSet;
    import java.sql.SQLException;
    import java.sql.Savepoint;

    public class jdbc05 {
        public static void main(String[] args) throws SQLException {
            Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcdemo", "root", "0009");
            PreparedStatement stat = conn.prepareStatement("update users set username=\"Java\" where id=?;");

            // 关闭自动提交，此时 通过conn.commit()进行提交
            conn.setAutoCommit(false);
            
            stat.setInt(1, 1);
            stat.executeUpdate();

            // 数据回滚点
            Savepoint point = conn.setSavepoint();
            // 数据回滚
            conn.rollback(point);
            stat.setInt(1, 1);
            stat.executeUpdate();
            // 提交数据
            conn.commit();

            stat.close();
            conn.close();
        }
    }
    ```