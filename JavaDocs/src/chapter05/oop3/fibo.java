package chapter05.oop3;

public class fibo {
    
    public int f(int i) {
        if (i<=2){
            return 1;
        }else{
            return f(i-1)+f(i-2);
        }
    }
}
