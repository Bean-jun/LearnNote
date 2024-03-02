package chapter07.error02;

class Dog{
    public void div(int x) throws Exception{
        if (x == 0){
            // 向上抛出异常
            throw new Exception("数字不能为0");
        }
        System.out.println(100/x);
    }
}
public class ErrorTest {
    public static void main(String[] args) {
        Dog g = new Dog();
        try {
            g.div(0);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
