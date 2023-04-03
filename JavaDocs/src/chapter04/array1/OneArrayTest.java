package chapter04.array1;

public class OneArrayTest {
    public static void main(String[] args) {
        // declare arrary
        // 不给数组个数，数组自动推导
        int[] a = new int[]{10, 12, 12, 1};
        // 给定数组个数
        int[] b = new int[10];

        int[] c = {10, 12, 12, 1};

        System.out.println(a[0]);
        System.out.println(b[0]);
        System.out.println(c[0]);
        System.out.println(c.length);

        for (int i = 0; i < c.length; i++) {
            System.out.println(c[i]);
        }
    }
}
