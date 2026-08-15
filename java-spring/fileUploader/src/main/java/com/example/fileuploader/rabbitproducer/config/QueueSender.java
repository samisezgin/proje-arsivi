package com.example.fileuploader.rabbitproducer.config;

import com.example.fileuploader.SafeFile;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class QueueSender {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Autowired
    private Queue queue;

    public void send(SafeFile safeFile) {
        rabbitTemplate.convertAndSend(this.queue.getName(), safeFile);
    }
}