package chapter07.date01;

import java.util.Calendar;

public class calenderDemo {
    public static void main(String[] args) {
        Calendar c = Calendar.getInstance();
        System.out.println(c.getTime());
        // 通过get方法 获取当前日期对象在今天的小时
        System.out.println(c.get(Calendar.HOUR_OF_DAY));
    }
}
