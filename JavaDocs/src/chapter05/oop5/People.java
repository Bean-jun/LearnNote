package chapter05.oop5;

public class People {
    String name;
    byte age;

    // 定义构造器
    public People() {
    }

    // 构造器重载
    public People(byte a) {
        age = a;
    }

    public void eat(String str) {
        System.out.println("吃" + str);
    }

    public static void main(String[] args) {
        People p1 = new People((byte)(1));
        System.out.println(p1.age);
        p1.eat("面包干");
        People p2 = new People();
        System.out.println(p2.age);
    }
}
