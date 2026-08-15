import java.util.*;
import java.util.concurrent.*;

public class TabularLogger {

    private static final ConcurrentMap<String, List<String>> logsPerThread = new ConcurrentHashMap<>();

    public static void log(String message) {
        String threadName = Thread.currentThread().getName();
        logsPerThread.computeIfAbsent(threadName, k -> Collections.synchronizedList(new ArrayList<>()))
                     .add(message);
    }

    public static void printTable() {
        List<String> threadNames = new ArrayList<>(logsPerThread.keySet());
        Collections.sort(threadNames); // İstersen alfabetik sırala

        // En uzun log sayısını bul
        int maxRows = logsPerThread.values().stream().mapToInt(List::size).max().orElse(0);

        // Başlık
        for (String thread : threadNames) {
            System.out.printf("%-20s", thread);
        }
        //System.out.println();

        // Satır satır yaz
        for (int i = 0; i < maxRows; i++) {
            for (String thread : threadNames) {
                List<String> logs = logsPerThread.get(thread);
                String log = (i < logs.size()) ? logs.get(i) : "";
                //System.out.printf("%-20s", log);
            }
            //System.out.println();
        }
    }
}
