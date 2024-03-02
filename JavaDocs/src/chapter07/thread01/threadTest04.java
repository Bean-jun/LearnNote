package chapter07.thread01;

public class threadTest04 implements Runnable {

    private int ticket = 10;

    // 出现线程数据异常问题
    // @Override
    // public void run() {
    //     ticket--;
    //     System.out.println(Thread.currentThread().getName() + "当前剩余数量：" + ticket);
    // }

    // 在【属性】和方法上面加 synchronized 同步来限制资源的访问。被 synchronized 包围的代码块称为同步代码块。
    // @Override
    // public void run() {
    //     synchronized (this) {
    //         ticket--;
    //         System.out.println(Thread.currentThread().getName() + "当前剩余数量：" + ticket);
    //     }
    // }

    // 在属性和【方法】上面加 synchronized 同步来限制资源的访问。
    @Override
    public synchronized void run() {
        ticket--;
        System.out.println(Thread.currentThread().getName() + "当前剩余数量：" + ticket);
    }

    public static void main(String[] args) {
        threadTest04 th = new threadTest04();
        new Thread(th).start();
        new Thread(th).start();
        new Thread(th).start();
        new Thread(th).start();
        new Thread(th).start();
        new Thread(th).start();
    }
}