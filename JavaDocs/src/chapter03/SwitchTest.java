package chapter03;

import java.util.Scanner;

public class SwitchTest {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int a = sc.nextInt();

        switch (a) {
            case 0:
                System.out.println("a:0");
                break;
            case 1:
                System.out.println("a:1");
                break;
            default:
                System.out.println("other");
        }

        sc.close();
    }
}
