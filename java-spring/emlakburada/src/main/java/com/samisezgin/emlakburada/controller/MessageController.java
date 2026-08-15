package com.samisezgin.emlakburada.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import com.samisezgin.emlakburada.model.Message;
import com.samisezgin.emlakburada.services.MessageService;

@Controller
@RequestMapping("/messages")
public class MessageController
{
	@Autowired
	private MessageService messageService;

	@GetMapping
	public ResponseEntity<List<Message>> getAll()
	{
		return new ResponseEntity<>(messageService.getAll(), HttpStatus.OK);
	}
}
