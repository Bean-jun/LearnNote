package chapter07.date01;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

public class jdk8timeDemo {
    public static void main(String[] args) {
        LocalDate nDate = LocalDate.now();
        System.out.println(nDate);
        System.out.println(nDate.getMonth());
        LocalTime nTime = LocalTime.now();
        System.out.println(nTime);
        LocalDateTime nDateTime = LocalDateTime.now();
        System.out.println(nDateTime);
    }
}
