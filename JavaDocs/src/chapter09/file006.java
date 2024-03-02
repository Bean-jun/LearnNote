package chapter09;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class file006 {
    public static void main(String[] args) throws IOException {
        BufferedInputStream r = new BufferedInputStream(new FileInputStream("./chapter09_file01.png"));
        BufferedOutputStream w = new BufferedOutputStream(new FileOutputStream("./chapter09_file03.png"));

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
