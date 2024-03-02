package chapter09;

import java.io.FileWriter;
import java.io.IOException;

public class file003 {
    public static void main(String[] args) {
        try {
            FileWriter w = new FileWriter("./chapter09_file01.txt");
            w.append("asss");
            w.append("d");
            w.append("ds");
            w.append("sdsfsdfsddddda阿是东方丽景阿萨德f");
            w.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
