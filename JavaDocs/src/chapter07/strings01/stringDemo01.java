package chapter07.strings01;

public class stringDemo01 {
    public static void main(String[] args) {
        String s = "hello";
        char[] c = s.toCharArray();
        for (int i = 0; i < c.length; i++) {
            System.out.println(c[i]);
        }
        String s2 = new String(c);
        System.out.println(s2);
        System.out.println(s2.charAt(1));
        System.out.println(s2.isEmpty());
    }
}
