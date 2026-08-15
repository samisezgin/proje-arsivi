import java.util.concurrent.*;

public class FastLoggerExample {
    static ConcurrentLinkedQueue<String> logQueue = new ConcurrentLinkedQueue<>();

    public static void log(String message) {
        logQueue.add(Thread.currentThread().getName() + ": " + message);
    }

    public static void flushLogs() {
        while (!logQueue.isEmpty()) {
            System.out.println(logQueue.poll()); // Burada yavaş olabilir ama artık thread'leri engellemez
        }
    }
}
