package chapter05.oop7;

public class Bank {
    private Customer[] customers;
    private int numberOfCustomer;

    public Bank() {
        this.customers = new Customer[100];
    }

    public void addCustomer(String f, String l) {
        Customer c = new Customer(f, l);
        this.customers[this.numberOfCustomer++] = c;
    }

    public int getNumOfCustomers() {
        return this.numberOfCustomer;
    }

    public Customer getCustomer(int index) {
        if (index < 0 || index >= this.numberOfCustomer) {
            System.out.println("当前用户不存在");
            return null;
        }
        return this.customers[index];
    }
}
