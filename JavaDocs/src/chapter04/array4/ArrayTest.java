package chapter04.array4;

import java.util.Arrays;

public class ArrayTest {
    public static void main(String[] args) {
        // 判断两个数组是否相等
        int[] a = new int[]{12, 2,3, 34};
        int[] b = new int[]{12, 2,3, 34};
        System.out.println(Arrays.equals(a, b));

        // 输出数组内的内容
        System.out.println(Arrays.toString(a));

        // 数组排序
        Arrays.sort(a);
        System.out.println(Arrays.toString(a));

        // 二分查找
        System.out.println(Arrays.binarySearch(a, 3));
        System.out.println(Arrays.binarySearch(a, 33));
    }
}
