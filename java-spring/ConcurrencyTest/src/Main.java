import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
//    public static void main(String[] args) {
//        //TIP Press <shortcut actionId="ShowIntentionActions"/> with your caret at the highlighted text
//        // to see how IntelliJ IDEA suggests fixing it.
//        System.out.printf("Hello and welcome!");
//
//        for (int i = 1; i <= 5; i++) {
//            //TIP Press <shortcut actionId="Debug"/> to start debugging your code. We have set one <icon src="AllIcons.Debugger.Db_set_breakpoint"/> breakpoint
//            // for you, but you can always add more by pressing <shortcut actionId="ToggleLineBreakpoint"/>.
//            System.out.println("i = " + i);
//        }
//    }

    public static void main(String[] args) throws InterruptedException {
         //Map<String, Integer> map = new HashMap<>(); // 👈 Bunu denersek hata olabilir
        Map<String, Integer> map = new ConcurrentHashMap<>();

        LongAdder longAdder = new LongAdder();
        longAdder.increment();
        longAdder.increment();
        System.out.println(longAdder.longValue());
        Runnable writer = () -> {
            for (int i = 0; i < 10_000_000; i++) {
                safePut(map,Thread.currentThread().getName() + "-" + i, i);
            }
        };

        Thread t1 = new Thread(writer, "T1");
        Thread t2 = new Thread(writer, "T2");
        Thread t3 = new Thread(writer, "T3");

        t1.start();
        t2.start();
        t3.start();

        t1.join();
        t2.join();
        t3.join();

        //FastLoggerExample.flushLogs();
        TabularLogger.printTable();
        System.out.println("Toplam entry sayısı: " + map.size());
    }

    private static void safePut(Map<String, Integer> map, String key, int i) {
        Integer prev = map.put(key, i);

        if (prev == null) {
            TabularLogger.log("PUT Succeeded: " + key);
        }
        else {
            TabularLogger.log("PUT Replaced existing: " + key);
        }
    }
}