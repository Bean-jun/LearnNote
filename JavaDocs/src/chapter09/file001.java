package chapter09;

import java.io.File;
import java.io.IOException;

public class file001 {
    public static void main(String[] args) throws IOException {
        File f = new File("./chapter09_file02.txt");
        System.out.println(f.getName());
        System.out.println(f.getAbsolutePath());
        System.out.println(f.exists());
        System.out.println(f.length());
        if (!f.exists()) {
            f.createNewFile();
        }

        String[] dir = f.list();
        System.out.println(dir);
    }
}
