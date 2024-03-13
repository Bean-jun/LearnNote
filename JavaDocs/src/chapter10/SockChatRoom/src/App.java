public class App {
    private static int serverPort = 7256;

    public static void main(String[] args) {
        if (args.length != 0 && args[0].equals("server")) {
            server.runner.Run(serverPort);
        } else {
            client.runner.Run("127.0.0.1", serverPort);
        }
    }
}
