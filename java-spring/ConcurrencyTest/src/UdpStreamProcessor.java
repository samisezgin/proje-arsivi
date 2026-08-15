import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.concurrent.*;
import java.util.concurrent.atomic.LongAdder;
import java.util.stream.IntStream;

public class UdpStreamProcessor {

    private static final int PORT = 5060;
    private static final int QUEUE_CAPACITY = 1000;
    private static final int THREAD_COUNT = 4;
    private static final ArrayBlockingQueue<String> messageQueue = new ArrayBlockingQueue<>(QUEUE_CAPACITY);
    private static final ConcurrentHashMap<String, CallSession> sessionMap = new ConcurrentHashMap<>();
    private static final LongAdder packetCount = new LongAdder();

    static void main() throws IOException {
        ExecutorService pool = Executors.newFixedThreadPool(THREAD_COUNT);

        // Worker thread'leri başlat
        IntStream.range(0, THREAD_COUNT).forEach(i -> pool.execute(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    String msg = messageQueue.take();
                    processMessage(msg);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }));

        // UDP socket ve paket alma döngüsü
        try (DatagramSocket socket = new DatagramSocket(PORT)) {
            byte[] buffer = new byte[2048];
            System.out.println("UDP Server started on port " + PORT);

            while (true) {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                socket.receive(packet);
                String data = new String(packet.getData(), 0, packet.getLength());
                packetCount.increment();

                // Mesajı kuyruğa ekle, eğer kuyruk doluysa mesajı at (offer)
                boolean offered = messageQueue.offer(data);
                if (!offered) {
                    System.out.println("Message queue full, dropping packet.");
                }
            }
        } finally {
            pool.shutdownNow();  // Program kapanırken pool'u kapat
        }
    }

    private static void processMessage(String msg) {
        String callId = extractCallId(msg);
        CallSession session = sessionMap.computeIfAbsent(callId, CallSession::new);
        session.handle(msg);
    }

    private static String extractCallId(String msg) {
        int start = msg.indexOf("Call-ID:");
        if (start == -1) return "unknown";
        int end = msg.indexOf("\n", start);
        return msg.substring(start + 8, end != -1 ? end : msg.length()).trim();
    }

    static class CallSession {
        private final String callId;
        private final LongAdder messageCount = new LongAdder();

        public CallSession(String callId) {
            this.callId = callId;
        }

        public void handle(String msg) {
            messageCount.increment();
            System.out.println("Call-ID [" + callId + "], Msg #" + messageCount.sum() + ": " + msg);
            // Burada daha ileri işleme yapılabilir
        }
    }
}
