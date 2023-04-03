package chapter03;

import java.util.Scanner;

public class ScanTest {
    public static void main(String[] args) {
        // 创建一个对象
        Scanner sc = new Scanner(System.in);
        // 获取数据
        System.out.println("请输入一个数据:");
        String line = sc.nextLine();

        System.out.println("获取数据结果为：" + line);
        // 关闭对象
        sc.close();
    }
}
