package chapter11;

import java.sql.*;

public class jdbc01 {
    public static void main(String[] args) throws SQLException {
            // 1. 创建连接
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306", "root", "0009");
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
