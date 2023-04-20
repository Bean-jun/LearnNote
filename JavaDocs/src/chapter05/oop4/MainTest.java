package chapter05.oop4;

public class MainTest {
    public static void main(String[] args) {
        Car c = new Car();
        People p = new People("张三", c);
        System.out.println(p.name + "购买的汽车容量:" + p.c.num);
    }
}
