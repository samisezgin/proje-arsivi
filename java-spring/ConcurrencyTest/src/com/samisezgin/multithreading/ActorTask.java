package com.samisezgin.multithreading;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.*;

import static com.samisezgin.multithreading.TaskType.*;

public class ActorTask implements Runnable {
    private final int actorId;
    private final ExecutorService pool;
    private final List<Integer> actorIds;
    private final AtomicInteger counter;
    private final ActorMessage message;

    public ActorTask(int actorId, ExecutorService pool, List<Integer> actorIds,
                     AtomicInteger counter, ActorMessage message) {
        this.actorId = actorId;
        this.pool = pool;
        this.actorIds = actorIds;
        this.counter = counter;
        this.message = message;
    }

    @Override
    public void run() {

        int limit=100_000;
        int currentCount = counter.incrementAndGet();
        if (currentCount > limit) return;

        Stats.record(actorId,message.getType());

        System.out.printf("Aktör-%d çalışıyor | Tür: %s | Mesaj: %s | Toplam: %d%n",
                actorId, message.getType(), message.getPayload(), currentCount);

        // Görev türüne göre işlem simülasyonu
        try {
            switch (message.getType()) {
                case CALC -> Thread.sleep(20);
                case LOG -> System.out.printf("Aktör-%d log: %s%n", actorId, message.getPayload());
                case UPDATE -> Thread.sleep(10);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }



        // Yeni görev üret ve rastgele bir aktöre gönder
        int nextId;
        do {
            nextId = actorIds.get(ThreadLocalRandom.current().nextInt(actorIds.size()));
        } while (nextId == actorId); // kendine paslama

        TaskType nextType = TaskType.values()[ThreadLocalRandom.current().nextInt(TaskType.values().length)];
        String nextPayload = "Görev#" + currentCount;

        ActorMessage newMsg = new ActorMessage(actorId, nextType, nextPayload);
        pool.submit(new ActorTask(nextId, pool, actorIds, counter, newMsg));
    }
}
