package com.samisezgin.multithreading;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class StatLogger {
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
    private final String logDirPath;
    private final AtomicInteger snapshotIndex = new AtomicInteger(1);

    public StatLogger(String logDirPath) {
        this.logDirPath = logDirPath;
        // Klasör yoksa oluştur
        File dir = new File(logDirPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }
    }

    public void start() {
        scheduler.scheduleAtFixedRate(this::logStats, 0, 5, TimeUnit.SECONDS);
    }

    public void shutdown() {
        scheduler.shutdownNow();
    }

    private void logStats() {
        String fileName = String.format("%s/log_%04d.txt", logDirPath, snapshotIndex.getAndIncrement());

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            writer.write("=== STAT LOG [" + System.currentTimeMillis() + "] ===\n");

            writer.write(">> Görev Türü Sayıları:\n");
            for (var entry : Stats.taskCounts.entrySet()) {
                writer.write("   - " + entry.getKey() + ": " + entry.getValue().get() + "\n");
            }

            writer.write(">> Toplam çalışan aktör sayısı: " + Stats.uniqueActors.size() + "\n");

            writer.write(">> Aktör Başına Çalışma Sayısı (ilk 10):\n");
            Stats.actorRuns.entrySet().stream()
                    .sorted((a, b) -> Integer.compare(b.getValue().get(), a.getValue().get()))
                    .limit(10)
                    .forEach(entry -> {
                        try {
                            writer.write("   - Actor-" + entry.getKey() + ": " + entry.getValue().get() + "\n");
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    });

            writer.write("\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}