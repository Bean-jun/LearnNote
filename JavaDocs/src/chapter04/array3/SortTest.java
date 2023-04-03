package chapter04.array3;

public class SortTest {
    public static void main(String[] args) {
        int[] arr = new int[] { 12, 23, 1, 2, 6 };

        for (int i = 0; i < arr.length; i++) {
            for (int j = i; j < arr.length; j++) {
                if (arr[i] > arr[j]) {
                    int a = arr[j];
                    arr[j] = arr[i];
                    arr[i] = a;
                }
            }
        }

        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
    }
}
