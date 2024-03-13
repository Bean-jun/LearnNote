package utils;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;

public class sockUtils {

    public static String getSocketMsg(Socket sock) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(sock.getInputStream()));
            char[] data = new char[10];
            int len;
            StringBuffer str = new StringBuffer();
            while ((len = in.read(data)) != -1) {
                str.append(data, 0, len);
                if (len < 10) {
                    break;
                }
            }
            return str.toString();
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

    public static void sendSocket(Socket sock, String str) {
        try {
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
            out.write(str);
            out.flush();
        } catch (IOException e) {
            System.out.println("send error -> " + e.getMessage());
            e.printStackTrace();
        }
    }

}
