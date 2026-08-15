package com.samisezgin.multithreading;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class Stats {
    public static final ConcurrentHashMap<Integer, AtomicInteger> actorRuns = new ConcurrentHashMap<>();
    public static final ConcurrentHashMap<TaskType, AtomicInteger> taskCounts = new ConcurrentHashMap<>();
    public static final Set<Integer> uniqueActors = ConcurrentHashMap.newKeySet();

    static {
        for (TaskType type : TaskType.values()) {
            taskCounts.put(type, new AtomicInteger(0));
        }
    }

    public static void record(int actorId, TaskType type) {
        actorRuns.computeIfAbsent(actorId, k -> new AtomicInteger(0)).incrementAndGet();
        taskCounts.get(type).incrementAndGet();
        uniqueActors.add(actorId); // <== burası önemli
    }

    public static void writeSummary(String filePath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            writer.write("=== OTURUM ÖZETİ ===\n");

            int totalTasks = taskCounts.values().stream().mapToInt(AtomicInteger::get).sum();
            writer.write(">> Toplam görev sayısı: " + totalTasks + "\n");
            writer.write(">> Toplam çalışan aktör sayısı: " + uniqueActors.size() + "\n");

            writer.write(">> En çok çalışan 10 aktör:\n");
            actorRuns.entrySet().stream()
                    .sorted((a, b) -> Integer.compare(b.getValue().get(), a.getValue().get()))
                    .limit(10)
                    .forEach(entry -> {
                        try {
                            writer.write("   - Actor-" + entry.getKey() + ": " + entry.getValue().get() + "\n");
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    });

            writer.write("\n>> Görev Türü Dağılımı:\n");
            for (var entry : taskCounts.entrySet()) {
                writer.write("   - " + entry.getKey() + ": " + entry.getValue().get() + "\n");
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
