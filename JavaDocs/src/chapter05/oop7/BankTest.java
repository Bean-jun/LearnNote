package chapter05.oop7;

public class BankTest {
    public static void main(String[] args) {
        Bank bank = new Bank();

        bank.addCustomer("张", "三");
        bank.addCustomer("李", "四");

        bank.getCustomer(0).setAccount(new Account(100));
        bank.getCustomer(0).getAccount().deposit(10);
        bank.getCustomer(0).getAccount().withdraw(90);
        bank.getCustomer(0).getAccount().withdraw(1000);
        bank.getCustomer(10).setAccount(new Account(200));
    }
}
