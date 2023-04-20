package chapter05.oop12;

class Bank {
    private Bank() {
    }

    private static Bank Instance = null;

    public static Bank getBank() {
        if (Instance == null) {
            Instance = new Bank();
        }
        return Instance;
    }
}

public class BankTest02 {
    public static void main(String[] args) {
        Bank b1 = Bank.getBank();
        Bank b2 = Bank.getBank();
        System.out.println(b1 == b2);
    }
}
