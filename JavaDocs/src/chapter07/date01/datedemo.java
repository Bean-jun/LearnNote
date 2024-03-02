package chapter07.date01;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class datedemo {
    public static void main(String[] args) {
        Date d = new Date();
        System.out.println(d.toString());
        System.out.println(d.getTime());
        java.sql.Date d2 = new java.sql.Date(1683468299278L);
        System.out.println(d2.toString());
        
        SimpleDateFormat s = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        // date -> str
        String ret = s.format(new Date());
        System.out.println(ret);
        // str -> date
        try {
            Date d3 = s.parse(ret);
            System.out.println(d3.toString());
        }
        catch (ParseException e) {
            e.printStackTrace();
        }
    }
}
