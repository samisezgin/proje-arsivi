package com.example.fileuploader;

import com.example.fileuploader.rabbitproducer.config.QueueSender;
import com.kanishka.virustotal.exception.APIKeyNotFoundException;
import com.kanishka.virustotal.exception.QuotaExceededException;
import com.kanishka.virustotal.exception.UnauthorizedAccessException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

@RestController
public class MainController {
    private final QueueSender queueSender;

    public MainController(QueueSender queueSender) {
        this.queueSender = queueSender;
    }


    @PostMapping(value = "/upload", consumes = "multipart/form-data")
    public String handleUpload(String description,
                               @RequestParam("file") MultipartFile file) throws IOException, QuotaExceededException, APIKeyNotFoundException, UnauthorizedAccessException {

        /* --------- PRODUCER CODE --------- */

        String fileName = file.getOriginalFilename();

        String message;

        File targetFile = new File("src/main/resources/" + fileName);

        Files.copy(
                file.getInputStream(),
                targetFile.toPath(),
                StandardCopyOption.REPLACE_EXISTING);
        int result = FileScanUtil.scanFile(targetFile);

        if (result == 400) {
            targetFile.delete();
            message = "Your file has virus, cant upload to the server!";
            return message;
        }

        if (result != 200) {
            targetFile.delete();
            message = "An error occurred while trying to upload the file, try again.";
            return message;
        }
        byte[] tempFileByteArray = file.getBytes();

        SafeFile safeFile = new SafeFile();
        safeFile.setFileName(fileName);
        safeFile.setFileByteArray(tempFileByteArray);
        queueSender.send(safeFile);
        Files.deleteIfExists(targetFile.toPath());
        message = "Your file is sent to upload queue successfully!";
        return message;


    }

}