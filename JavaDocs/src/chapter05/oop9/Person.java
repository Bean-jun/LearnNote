package chapter05.oop9;

public class Person {
    public Person() {
        System.out.println("我是父类的空构造器");
    }

    public Person(String xx) {
        System.out.println("我是父类有参数的构造器" + xx);
    }
}

class Student extends Person {
    public Student() {
        // super();
    }

    public static void main(String[] args) {
        System.out.println("hello world");
        Student s = new Student();
        System.out.println(s);
    }
}