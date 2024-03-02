package chapter07.thread01;

class AppT01 extends Thread{
    @Override
    public void run(){
        try {
            Thread.sleep(1000);
            System.out.println("sub thread");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

public class threadTest03 {
    public static void main(String[] args) {
        AppT01 a1 = new AppT01();
        a1.start();
        try {
            a1.join();
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("main thread 01");
        AppT01 a2 = new AppT01();
        a2.start();
        System.out.println("main thread 02");
    }
}
