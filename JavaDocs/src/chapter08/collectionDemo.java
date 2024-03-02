package chapter08;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

public class collectionDemo {
    public static void main(String[] args) {
        Collection coll = new ArrayList();
        coll.add(12);
        coll.add("tom");
        coll.add("中文");
        System.out.println(coll.size());
        System.out.println(coll.isEmpty());
        System.out.println(coll);
        coll.remove(12);
        System.out.println(coll);

        // 迭代器
        Iterator itor = coll.iterator();
        while (itor.hasNext()) {
            System.out.println(itor.next());
        }

        // 增强for循环
        for (Object obj : coll) {
            System.out.println(obj);
        }
    }
}
