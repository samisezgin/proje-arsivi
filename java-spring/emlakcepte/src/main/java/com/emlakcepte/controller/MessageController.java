package com.emlakcepte.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.emlakcepte.model.Message;
import com.emlakcepte.service.MessageService;

@RestController
@RequestMapping("/messages")
public class MessageController
{
	@Autowired
	private MessageService messageService;
	
	
	@GetMapping
	public List<Message> getAll()
	{
		System.out.println("HTTP-GET MessageController called.");
		return messageService.getAll();
	}
	
	@PostMapping
	public ResponseEntity<Message> create(@RequestBody Message message)
	{
		System.out.println("HTTP-POST MessageController -> Create Message called.");
		messageService.create(message);
		return new ResponseEntity<>(message, HttpStatus.CREATED);
	}
	
	@PutMapping("/{title}")
	public ResponseEntity<Message> update(@PathVariable String title, @RequestBody Message message)
	{
		System.out.println("HTTP-PUT MessageController -> Update Message called.");
		messageService.update(title, message);
		return new ResponseEntity<>(message,HttpStatus.ACCEPTED);
	}
	
	@DeleteMapping("/{title}")
	public ResponseEntity<String> delete(@PathVariable String title)
	{
		System.out.println("HTTP-DELETE MessageController -> Delete Message called.");
		messageService.delete(title);
		return new ResponseEntity<>(title,HttpStatus.OK);
	}
}
