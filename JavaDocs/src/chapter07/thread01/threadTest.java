package chapter07.thread01;

class App extends Thread {
    @Override
    public void run() {
        System.out.println("get url");
    }
}

public class threadTest {
    public static void main(String[] args) {
        App app = new App();
        app.start();
    }
}
