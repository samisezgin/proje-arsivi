package com.emlakcepte.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.emlakcepte.model.Message;
import com.emlakcepte.repository.MessageRepository;

@Service
public class MessageService
{
	@Autowired
	private MessageRepository messageRepository;

	public List<Message> getAll()
	{
		return messageRepository.getAll();
	}

	public void create(Message message)
	{
		messageRepository.create(message);
	}

	public void update(String title, Message message)
	{
		messageRepository.update(title, message);
	}

	public void delete(String title)
	{
		messageRepository.delete(title);
	}
}
