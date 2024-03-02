package chapter09;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class file005 {
    public static void main(String[] args) throws IOException {
        FileInputStream r = new FileInputStream("./chapter09_file01.png");
        FileOutputStream w = new FileOutputStream("./chapter09_file02.png");

        byte[] data = new byte[2];
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
