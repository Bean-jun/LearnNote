package chapter03;

public class LoopTest {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            System.out.println("i value:" + i);
        }

        int a = 10;
        while (a > 0) {
            System.out.println("a value:" + a);
            a -= 1;
        }

        int b = 10;
        do {
            System.out.println("c value:" + b);
            b -= 1;
        } while (b > 0);

        for (;;){
            System.out.println("死循环");
        }
    }
}
