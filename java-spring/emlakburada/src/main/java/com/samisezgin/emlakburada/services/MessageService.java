package com.samisezgin.emlakburada.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.samisezgin.emlakburada.model.Message;
import com.samisezgin.emlakburada.repository.MessageRepository;

@Service
public class MessageService
{
	@Autowired
	private MessageRepository messageRepository;

	public List<Message> getAll()
	{
		return messageRepository.findAll();
	}
}
