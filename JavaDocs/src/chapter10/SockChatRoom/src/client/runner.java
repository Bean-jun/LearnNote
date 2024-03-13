package client;

public class runner {
    public static void Run(String host, int port){
        System.out.println("chat client running...");
        new boot().RunBoot(host, port);
    }
}
