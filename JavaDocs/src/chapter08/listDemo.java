package chapter08;

import java.util.ArrayList;
import java.util.List;

public class listDemo {
    public static void main(String[] args) {
        List list = new ArrayList();
        list.add("A");
        list.add("B");
        list.add(2);
        list.add(0, "C");
        System.out.println(list);
    }
}
