package chapter08;

import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class setDemo {
    public static void main(String[] args) {
        Set set = new HashSet();
        set.add(10);
        set.add(20);
        set.add(10);
        System.out.println(set.size());
        System.out.println(set);

        System.out.println(String.valueOf("ab").hashCode());
        
        Iterator iter = set.iterator();
        while (iter.hasNext()){
            System.out.println(iter.next());
        }
    }
}
