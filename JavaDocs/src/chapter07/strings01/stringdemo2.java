package chapter07.strings01;

public class stringdemo2 {
    String str = "good";

    public void change(String str){
        str = "????";
    }
    public static void main(String[] args) {
        stringdemo2 s = new stringdemo2();
        System.out.println(s.str);
        s.change("best");
        System.out.println(s.str);
    }
}
