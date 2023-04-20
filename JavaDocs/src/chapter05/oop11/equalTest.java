package chapter05.oop11;

public class equalTest {
    String name;
    int age;

    public equalTest(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // 重写equals后 两个对象比较
    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }

        if (obj instanceof equalTest) {
            equalTest objE = (equalTest) obj;
            return this.age == objE.age;
        }

        return false;
    }

}

class Main {
    public static void main(String[] args) {
        equalTest e1 = new equalTest("张三", 10);
        equalTest e2 = new equalTest("李四", 10);
        // Object equals方法比较e1 e2栈地址
        // 重写equals方法，比较两个对象的值
        boolean x = e1.equals(e2);
        System.out.println("e1 == e2 ?" + x);
    }
}