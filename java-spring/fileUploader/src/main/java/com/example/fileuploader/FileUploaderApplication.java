package com.example.fileuploader;

import org.springframework.amqp.rabbit.annotation.EnableRabbit;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@EnableRabbit
@SpringBootApplication
public class FileUploaderApplication {
	public static void main(String[] args) {
		SpringApplication.run(FileUploaderApplication.class, args);
	}
}
