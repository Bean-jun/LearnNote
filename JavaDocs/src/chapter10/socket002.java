package chapter10;
/*
 * tcp client
 */
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;

public class socket002 {
    public static void main(String[] args) throws UnknownHostException, IOException {
        Socket sock = new Socket("127.0.0.1", 8081);
        BufferedReader bf = new BufferedReader(new InputStreamReader(sock.getInputStream()));

        char[] data = new char[20];
        StringBuilder b = new StringBuilder();
        int len;
        while ((len = bf.read(data)) != -1) {
            b.append(data, 0, len);
            System.out.println(b.toString());
            b.delete(0, len);
        }

        bf.close();
        sock.close();
    }
}
