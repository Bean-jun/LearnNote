package chapter06.oop2;

public class Man extends Person {
    @Override
    public void eat() {
        System.out.println("男人吃饭");
    }

    public static void main(String[] args) {
        Man man = new Man();
        man.eat();
    }
}
