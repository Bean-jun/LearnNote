package chapter06.oop1;

class Bank {

    // 非静态代码块
    {
        System.out.println("我是非静态代码块");
    }

    // 静态代码块
    static {
        System.out.println("我是静态代码块");
    }
}

public class staticTest {
    public static void main(String[] args) {
        Bank b = new Bank();
        System.out.println(b);
    }
}
