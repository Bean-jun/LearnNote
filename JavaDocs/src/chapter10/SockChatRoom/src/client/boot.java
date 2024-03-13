package client;

import java.io.IOException;
import java.net.Socket;
import java.util.Scanner;

import utils.sockUtils;

public class boot {
    public void RunBoot(String host, int port) {
        Socket sock;
        try {
            sock = new Socket(host, port);
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
        // 获取消息
        Thread getThread = new Thread(() -> {

            while (true) {
                if (sock.isClosed()) {
                    break;
                }
                String msg = sockUtils.getSocketMsg(sock);
                if (msg.isEmpty()){
                    continue;
                }
                System.out.println("获取的消息内容为:" + msg);
            }
        });
        // 发送消息
        Thread setThread = new Thread(() -> {
            Scanner in = new Scanner(System.in);
            while (true) {
                System.out.println("请输入你想发送的消息:");
                String msg = in.nextLine();
                sockUtils.sendSocket(sock, msg);
                if (msg.equals("bye")) {
                    break;
                }
            }
            in.close();
        });
        getThread.start();
        setThread.start();
        try {
            setThread.join();
            sock.close();
        } catch (InterruptedException | IOException e) {
            e.printStackTrace();
        }
    }
}
