package server;

import java.net.Socket;
import java.util.ArrayList;

import utils.sockUtils;

public class roomImpl {
    private ArrayList<Socket> roomList = new ArrayList<Socket>();

    public boolean PutUser(Socket sock) {
        return this.roomList.add(sock);
    }

    public boolean DeleteUser(Socket sock) {
        return this.roomList.remove(sock);
    }

    public void BroasdMessage(Socket sock, String msg) {
        for (Socket socket : roomList) {
            if (!socket.equals(sock)) {
                sockUtils.sendSocket(socket, msg);
            }
        }
    }

}
