package chapter05.oop1;

public class Phone {

    // 属性
    String name;// 品牌
    double price;// 价格

    // 方法
    public void call() {
        System.out.println("打电话");
    }

    public void sendMsg(String msg) {
        System.out.println("发送消息结果为：" + msg);
    }
}