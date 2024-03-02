package chapter08;

import java.util.HashMap;
import java.util.Map;

public class mapTest {
    public static void main(String[] args) {
        Map map = new HashMap();
        map.put("name", "tom");
        map.put("age", 12);
        System.out.println(map);
        System.out.println(map.keySet());
    }
}
