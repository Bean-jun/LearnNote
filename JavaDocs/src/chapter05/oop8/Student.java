package chapter05.oop8;

public class Student extends Person {
    public Student(String name, int age) {
        super(name, age);
    }

    @Override
    public String showInfo() {
        return "我在重写父类的方法";
    }

    public static void main(String[] args) {
        Student s = new Student("张三", 20);
        System.out.println(s.showInfo());
    }
}
