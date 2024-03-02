package chapter07.thread01;

import java.util.concurrent.Callable;
import java.util.concurrent.FutureTask;

class AppCall implements Callable {
    @Override
    public Object call() throws Exception {
        int sum = 0;
        for (int i = 0; i <= 100; i++) {
            Thread.sleep(100);
            sum += i;
        }
        return sum;
    }
}

public class threadTest06 {
    public static void main(String[] args) {
        AppCall app = new AppCall();
        FutureTask ftask = new FutureTask(app);
        Thread t = new Thread(ftask);
        t.start();
        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("main over");
        try {
            System.out.println("thread result:" + ftask.get());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
