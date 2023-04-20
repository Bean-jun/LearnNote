package chapter05.oop10;

public class Person {
    public void say(String msg) {
        System.out.println("person say" + msg);
    }

    public void eat() {
        System.out.println("person eat");
    }
}

class Man extends Person {
    public void say(String msg) {
        System.out.println("man say" + msg);
    }

    public void eat() {
        System.out.println("man eat");
    }

    public void sleep() {
        System.out.println("man sleep");
    }
}

class Woman extends Person {
    public void say(String msg) {
        System.out.println("Woman say" + msg);
    }

    public void eat() {
        System.out.println("Woman eat");
    }

    public void watch() {
        System.out.println("woman watch");
    }
}

class Programmer {
    public void run(Person p) {
        p.say("hello world");
        p.eat();

        // 尝试 向下转型
        if (p instanceof Man) {
            // 判断当前类型是man类型，进行转换
            Man mp = (Man)p;
            mp.sleep();
        }

        if (p instanceof Woman){
            Woman wp = (Woman)p;
            wp.watch();
        }
    }
}

class PersonTest {
    public static void main(String[] args) {
        Programmer p = new Programmer();
        // p.run中调用的say、eat还是根据当前对象来进行调用的
        // 初始化Person类
        p.run(new Person());
        // 初始化Man类，其为Person的子类，
        // 故此处为向上转型
        p.run(new Man());
        // 初始化Woman类，其为Person的子类，
        // 故此处为向上转型
        p.run(new Woman());
    }
}