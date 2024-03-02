package chapter10;
/**
 * tcp server
 */
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class socket001 {
    public static void ReadChar(Socket sock) throws IOException {
        BufferedReader inp = new BufferedReader(new InputStreamReader(sock.getInputStream(), "GBK"));

        int size = 20;
        int len = 0;
        int lineSize;
        char[] data = new char[size];
        StringBuilder b = new StringBuilder();
        while (true) {
            lineSize = 0;
            while ((len = inp.read(data)) != -1) {
                for (int i = 0; i < len; i++) {
                    b.append(data[i]);
                    data[i] = ' ';
                }
                lineSize += len;
                if (len < size) {
                    break;
                }
            }
            System.out.println(b.toString());
            b.delete(0, lineSize);
        }

    }

    public static void PutChar(Socket sock) throws IOException, InterruptedException {
        BufferedWriter outp = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
        while (true) {
            outp.write("ping " + (int) (Math.random() * 100));
            outp.flush();
            Thread.sleep(1000);
        }
    }

    public static void HanderSock(Socket sock) throws IOException {
        try {
            System.out.println("start conn...");
            new Thread(() -> {
                try {
                    ReadChar(sock);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }).start();
            new Thread(() -> {
                try {
                    PutChar(sock);
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }).start();

        } catch (Exception e) {
            e.printStackTrace();
            sock.close();
        }
    }

    public static void main(String[] args) {
        try (ServerSocket s = new ServerSocket(8081)) {
            while (true) {
                Socket sock = s.accept();
                new Thread(() -> {
                    try {
                        HanderSock(sock);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}