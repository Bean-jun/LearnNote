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
