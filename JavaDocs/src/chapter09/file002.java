package chapter09;

import java.io.FileReader;
import java.io.IOException;

public class file002 {
    public static void main(String[] args) throws IOException {
        FileReader f = new FileReader("./chapter09_file01.txt");
        // System.out.println((char) f.read());
        int data = f.read();
        while (true) {
            if (data == -1) {
                break;
            }
            System.out.print((char)data);
            data = f.read();
        }
        f.close();
    }
}
