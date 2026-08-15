package com.example.fileuploader.rabbitconsumer;

import com.example.fileuploader.S3Util;
import com.example.fileuploader.SafeFile;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.nio.file.Files;

@Component
public class FileListener {

    @RabbitListener(queues = "${fileupload.rabbitmq.queue}")
    public void receive(@Payload SafeFile fileBody) {

        File file = new File(fileBody.getFileName());
        FileInputStream inputStream = null;
        try {
            OutputStream os = new FileOutputStream(file);
            os.write(fileBody.getFileByteArray());
            os.close();
            inputStream = new FileInputStream(file);
        } catch (Exception ignored) {

        }
        System.out.println("Message " + fileBody.getFileName());
        if (inputStream != null) {
            /* --------- CONSUMER CODE --------- */
            try {
                S3Util.uploadFile(fileBody.getFileName(), inputStream);
                Files.deleteIfExists(file.toPath());
                System.out.println("Your file has been uploaded successfully!");
            } catch (Exception ex) {
                System.out.println("Error uploading file: " + ex.getMessage());
            }
        }
    }

}