package server;

public class runner {
    public static void Run(int port) {
        System.out.println("chat room running on port: " + port + "...");
        new boot().RunBoot(port);
    }
}
