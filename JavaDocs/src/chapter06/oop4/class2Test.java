package chapter06.oop4;

interface Fx {
    public void say();
}

public class class2Test {
    public static void main(String[] args) {
        new Fx() {
            public void say(){
                // 由此可以确定  是创建了一个内部类
                System.out.println(this.getClass());
                System.out.println(this.getClass().getSuperclass());
                System.out.println("say....");
            }
        }.say();
    }
}
