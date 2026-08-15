package com.samisezgin.multithreading;

public class ActorMessage {
    private final int fromActorId;
    private final TaskType taskType;
    private final String payload;

    public ActorMessage(int fromActorId, TaskType taskType, String payload) {
        this.fromActorId = fromActorId;
        this.taskType = taskType;
        this.payload = payload;
    }

    public int getFromActorId() {
        return fromActorId;
    }
    public TaskType getType() {
        return taskType;
    }
    public String getPayload() {
        return payload;
    }
}
