package chapter05.oop7;

public class Account {
    private double balance;

    public double getBalance() {
        return balance;
    }

    public Account(double balance) {
        this.balance = balance;
    }

    // 存钱
    public void deposit(double amt) {
        if (amt > 0) {
            this.balance += amt;
            System.out.println("成功存入：" + amt + "剩余：" + this.balance);
        }
    }

    // 取钱
    public void withdraw(double amt) {
        if (amt > 0 && this.balance >= amt) {
            this.balance -= amt;
            System.out.println("成功取出：" + amt + "还剩余：" + this.balance);
        } else {
            System.out.println("余额不足");
        }
    }
}
