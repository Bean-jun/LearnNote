package server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import utils.sockUtils;

public class boot {
    private roomImpl room = new roomImpl();

    public void RunBoot(int port) {
        try (ServerSocket sock = new ServerSocket(port)) {
            while (true) {
                Socket socket = sock.accept();
                this.room.PutUser(socket);
                new Thread(() -> {
                    while (true) {
                        if (sock.isClosed()) {
                            System.out.println("server sock close");
                            break;
                        }
                        // 获取用户发送消息
                        String msg = sockUtils.getSocketMsg(socket);
                        if (msg.isEmpty()) {
                            continue;
                        }

                        System.out.println(msg);

                        // 用户退出聊天室
                        if (msg.equals("bye")) {
                            this.room.DeleteUser(socket);
                            try {
                                socket.close();
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                            break;
                        }
                        // 用户广播自己的消息
                        this.room.BroasdMessage(socket, msg);
                    }
                }).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
