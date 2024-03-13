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
        Connection conn = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/jdbcdemo", "root", "0009");
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
