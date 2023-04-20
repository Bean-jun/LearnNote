package chapter06.oop6;

public class WrapperTest {
    public static void main(String[] args) {
        // 包装类的自动装箱 拆箱

        // 装箱
        Integer a = 5;
        System.out.println(a + "<>" + a.intValue());
        // 拆箱
        int b = a;
        System.out.println(b);

        // 包装类列举
        // Boolean -> boolean
        // Character->char
        // Byte -> byte
        // Short -> short
        // Integer -> int
        // Long -> long
        // Float -> float
        // Double -> double
        System.out.println(Byte.MAX_VALUE);
    }
}
