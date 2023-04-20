package chapter05.oop12;

class Bank {

    // 构造器私有化，禁止被new出来
    private Bank() {
    }

    private static Bank Instance = new Bank();

    // 通过静态方法返回当前对象
    public static Bank getBank() {
        return Instance;
    }
}

public class BankTest {
    public static void main(String[] args) {
        Bank b1 = Bank.getBank();
        Bank b2 = Bank.getBank();
        System.out.println(b1 == b2);
    }
}
