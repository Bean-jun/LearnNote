package chapter04.array2;

public class OneArrayTest {
    public static void main(String[] args) {
        // declare arrary
        int[][] a = new int[][] {
                { 10, 12, 34 },
                { 12, 43, 22 },
                { 12, 43, 22, 232 },
        };

        System.out.println(a.length);
        System.out.println(a[0].length);

        for (int i = 0; i < a.length; i++) {
            System.out.println("....." + a[i].length);
            for (int j = 0; j < a[i].length; j++) {
                System.out.print(a[i][j] + " ");
            }
            System.out.println();
        }

        System.out.println("--------------");

        int[][] b = new int[3][4];
        for (int i = 0; i < b.length; i++) {
            System.out.println("....." + b[i].length);
            for (int j = 0; j < b[i].length; j++) {
                System.out.print(b[i][j] + " ");
            }
            System.out.println();
        }
    }
}
