package chapter08;

class Add<T> {
    private T a;
    private T b;

    public T getA() {
        return a;
    }

    public void setA(T a) {
        this.a = a;
    }

    public T getB() {
        return b;
    }

    public void setB(T b) {
        this.b = b;
    }

    public void result() {
        System.out.println(this.a);
        System.out.println(this.b);
    }
}

public class gen001 {
    public static void main(String[] args) {
        Add<String> a = new Add<>();
        a.setA("1afdsf00");
        a.setB("202002asdfased");
        a.result();
    }
}
