package chapter07.thread01;

class App implements Runnable {

    @Override
    public void run() {
        try {
            Thread.sleep(1000);
            System.out.println("this is :" + Thread.currentThread().getName());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}

public class threadTest01 {
    public static void main(String[] args) {
        App app = new App();
        new Thread(app).start();
        System.out.println("main thread:" + Thread.currentThread().getName());
    }
}