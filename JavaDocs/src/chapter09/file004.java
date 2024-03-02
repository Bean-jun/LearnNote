package chapter09;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class file004 {
    public static void main(String[] args) throws IOException {
        FileReader r = new FileReader("./chapter09_file01.txt");
        FileWriter w = new FileWriter("./chapter09_file02.txt");

        char[] data = new char[2];
        int len;
        while (true) {
            len = r.read(data);
            if (len == -1) {
                break;
            }
            w.write(data);
        }

        r.close();
        w.close();
    }
}
