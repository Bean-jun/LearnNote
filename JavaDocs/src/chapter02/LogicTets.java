package chapter02;

public class LogicTets {
    public static void main(String[] args) {
        int a = 1;
        boolean b = false;
        // 由于使用&&短路与，故a不会++ a的值不变
        if (b && (a++ > 0)) {
            System.out.println("if " + a);
        } else {
            System.out.println("else " + a);
        }

        // 由于使用&非短路与，故a会++ a的值变为2
        if (b & (a++ > 0)) {
            System.out.println("if " + a);
        } else {
            System.out.println("else " + a);
        }

        int c = 1;
        boolean d = true;
        // 由于使用|短路或，故c不会++ c的值不变
        if (d || (c++ > 0)) {
            System.out.println("if " + c);
        } else {
            System.out.println("else " + c);
        }

        // 由于使用|非短路或，故c会++ c的值变为2
        if (d | (c++ > 0)) {
            System.out.println("if " + c);
        } else {
            System.out.println("else " + c);
        }
    }
}
