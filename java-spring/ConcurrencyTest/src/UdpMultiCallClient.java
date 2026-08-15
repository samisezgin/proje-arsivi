import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class UdpMultiCallClient {

    private static final String SERVER_HOST = "localhost"; // Server IP veya hostname
    private static final int SERVER_PORT = 5060;
    private static final int CALL_COUNT = 1000;    // Kaç farklı çağrı simüle edilecek
    private static final int MSGS_PER_CALL = 100; // Her çağrı için kaç mesaj gönderilecek
    private static final int THREADS = 100;       // Paralel gönderim için thread sayısı

    public static void main(String[] args) throws Exception {
        long startTime = System.nanoTime();
        InetAddress serverAddress = InetAddress.getByName(SERVER_HOST);
        ExecutorService pool = Executors.newFixedThreadPool(THREADS);

        // CALL_COUNT farklı çağrı için ayrı thread'de mesaj gönderimi
        IntStream.range(0, CALL_COUNT).forEach(callIndex -> pool.submit(() -> {
            try (DatagramSocket socket = new DatagramSocket()) {
                String callId = "call-" + callIndex;

                for (int i = 1; i <= MSGS_PER_CALL; i++) {
                    String message = "Call-ID: " + callId + "\nMessage number: " + i;
                    byte[] data = message.getBytes();

                    DatagramPacket packet = new DatagramPacket(data, data.length, serverAddress, SERVER_PORT);
                    socket.send(packet);

                    System.out.println("Sent to server: " + message);

                    Thread.sleep(100); // Mesajlar arası ufak gecikme (opsiyonel)
                }

                long endTime = System.nanoTime();
                long elapsedTime = endTime - startTime;
                double elapsedSeconds = elapsedTime / 1_000_000_000.0;
                System.out.println("Elapsed time: " + elapsedSeconds + " seconds");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }));

        pool.shutdown();
    }
}
