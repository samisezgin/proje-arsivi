package com.samisezgin.multithreading;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        int actorCount = 30_000;
        List<Integer> actorIds = new ArrayList<>(actorCount);
        for (int i = 0; i < actorCount; i++) {
            actorIds.add(i);
        }

        int threadPoolSize = Runtime.getRuntime().availableProcessors();
        ExecutorService pool = Executors.newFixedThreadPool(threadPoolSize);

        AtomicInteger counter = new AtomicInteger(0);

        StatLogger logger = new StatLogger("logs");
        logger.start();

        // Başlangıçta her aktöre 1 görev göndererek garantile
        for (int actorId : actorIds) {
            TaskType randomType = TaskType.values()[ThreadLocalRandom.current().nextInt(TaskType.values().length)];
            ActorMessage msg = new ActorMessage(-1, randomType, "Initial task");
            pool.submit(new ActorTask(actorId, pool, actorIds, counter, msg));
        }

        // Programı 60 saniye çalıştır
        Thread.sleep(60_000);

        pool.shutdown();
        if (!pool.awaitTermination(10, TimeUnit.SECONDS)) {
            pool.shutdownNow();
        }

        logger.shutdown();

        // Kapanışta summary yazdır
        Stats.writeSummary("logs/summary.txt");
    }
}

