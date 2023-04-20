package chapter06.oop4;

public class ClassTest{
    public static void main(String[] args) {
        // 创建一个匿名对象
        // 通过这种方式，其实是创建的Object的子类，并实现了一个show方法
        // 由于是匿名类，没有名称，故调用可以直接在创建的对象上调用
        new Object(){
            public void show(){
                System.out.println("我是show方法");
            }
        }.show();
    }
}