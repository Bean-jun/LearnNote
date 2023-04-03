1. 环境配置

    ```shell
    # 设置jdk的bin目录到path环境变量
    JAVA_HOME = C:\Program Files\Microsoft\jdk-11.0.16.101-hotspot
    PATH = %JAVA_HOME%\bin
    ```

2. helloworld

    ```java
    class HelloWorld{
        public static void main(String[] args) {
            System.out.println("hello world");
        }
    }
    ```

3. javadoc

    javadoc -d 目录 -encoding utf8 -version -author 源文件

    ```java
    // 通过编辑下方注解 可以生成对应文档
    // javadoc -d dir -encoding utf8 -version -author chapter01\HelloWorld.java

    /**
     * @author Bean-jun
     * @version 1.0
     * 这是一个文档
     */
    class HelloWorld {
        public static void main(String[] args) {
            System.out.println("hello world");
        }
    }
    ```

4. 变量

    ```java
    // 数据类型 变量名 = 变量值

    // 自动类型提升
    byte、short、char --> int --> long --> float --> double

    // 基础数据类型
    byte、short、char、int、long、float、double
    // 引用数据类型
    类、数组、接口、枚举、注解、记录

    // 强制转换
    类型 变量 = (类型)变量;

    // 一个有趣的例子->byte和short都存在这种情况，默认加的数据值是一个int类型
    short a = 10;
    a = a + 10; // 编译异常
    a += 10;    // 编译成功 等价于 a = short(a + 10);
    ```

5. String类型只能和基础数据类型做连接运算

    ```java
    public class StringTest {
        public static void main(String[] args) {
            String str1 = "hello world";
            System.out.println("str value:"+str1);
            System.out.println('a'+1+"sss");

            float a = 10;
            a = a + 10;
            // a += 12;
            // a = (byte) (a + 12);
            System.out.println(a);
        }
    }
    ```

6. 条件运算符

    ```java
    // (条件表达式)？表达式1：表达式2
    public class ConditionTest {
        public static void main(String[] args) {
            int a = 10;
            int b = (a == 10) ? 12 : 20;
            System.out.println("b value:" + b);// b value:12
        }
    }
    ```

7. 逻辑运算符

    ```java
    // &、&&
    //     都是与运算，后者是短路与，即左边为false时，后面不会继续执行
    // |、||
    //     都是或运算，后者是短路或，即左边为true时，后面不会继续执行
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
    ```

8. 位运算符 | & ^

    ```java
    // |和&在前面提到过是逻辑运算符，但是在对于非boolean类型时，属于位运算符
    public class BitTest {
        public static void main(String[] args) {
            int a = 1; // 0b01
            int b = 2; // 0b10
            System.out.println(a & b); // ob00
            System.out.println(a | b); // 0b11
        }
    }
    ```

9. 条件语句

    ```java
    public class IfElse {
        public static void main(String[] args) {
            int a = 0;
            if (a > 2) {
                System.out.println("a>2");
            } else if (a > 1) {
                System.out.println("1<a<=2");
            } else {
                System.out.println("a<=1");
            }
        }
    }
    ```

10. Scanner使用

    ```java
    import java.util.Scanner;

    public class ScanTest {
        public static void main(String[] args) {
            // 创建一个对象
            Scanner sc = new Scanner(System.in);
            // 获取数据
            System.out.println("请输入一个数据:");
            String line = sc.nextLine();

            System.out.println("获取数据结果为：" + line);
            // 关闭对象
            sc.close();
        }
    }
    ```

11. Math使用

    ```java
    public class MathTest {
        public static void main(String[] args) {
            double a = Math.random() * 100;
            System.out.println((int)a);
        }
    }
    ```

12. switch

    ```java
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
    ```

13. 循环

    ```java
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
    ```

14. 一维数组 -> 引用类型

    ```java
    // 定义数组
    // 整型数组元素的默认初始化值: 0
    // 浮点型数组元素的默认初始化值: 0.0
    // 字符型数组元素的默认初始化值: 0
    // boolean型数组元素的默认初始化值: false
    // 引用数据类型数组元素的默认初始化值: null
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
        }
    }
    ```

    ```java
    // 冒泡排序
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
    ```

15. 二维数组

    ```java
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
    ```

16. Arrays工具类

    ```java
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
    ```

























