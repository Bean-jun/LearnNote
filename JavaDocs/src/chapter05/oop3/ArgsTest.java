package chapter05.oop3;

public class ArgsTest {
    public void pprint01(int ... num) {
        System.out.println(num);
    }

    public void pprint02(double[] num) {
        System.out.println(num);
    }

    public static void main(String[] args) {
        ArgsTest a= new ArgsTest();
        a.pprint01(1,2,3,4,5);
        double[] b = new double[]{12.1,  121.2, 1.1};
        a.pprint02(b);
    }
}
