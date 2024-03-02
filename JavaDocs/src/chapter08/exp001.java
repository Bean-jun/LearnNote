package chapter08;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Student {
    private String name;
    private int age;

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    @Override
    public String toString() {
        return this.name + " " + this.age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o instanceof Student) {
            Student s = (Student) o;
            if (this.age == s.age) {
                return true;
            }
        }
        return false;
    }
}

public class exp001 {
    public static void main(String[] args) {
        List list = new ArrayList();
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.println("1:继续录入\n0:结束录入:");
            String line = sc.next();
            if (line.equals("0")) {
                break;
            }
            System.out.println("请输入姓名：");
            String name = sc.next();
            System.out.println("请输入年龄：");
            int age = sc.nextInt();
            list.add(new Student(name, age));
        }
        sc.close();

        for (Object s : list) {
            System.out.println(s);
        }
    }
}
