package chapter05.oop2;

public class overloadTest {
    public void add(int i, int j) {
        System.out.println(i + j);
    }

    public void add(String i, String j) {
        System.out.println(i + j);

    }

    public static void main(String[] args) {
        overloadTest o = new overloadTest();
        o.add(10, 30);
        o.add("hello", "world");
    }
}
