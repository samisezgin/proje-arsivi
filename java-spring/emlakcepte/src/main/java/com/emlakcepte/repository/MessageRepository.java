package com.emlakcepte.repository;

import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Component;

import com.emlakcepte.model.Message;

@Component
public class MessageRepository
{
	private static List<Message> messageList = new ArrayList<>();

	public void create(Message message)
	{
		messageList.add(message);
	}

	public List<Message> getAll()
	{
		return messageList;
	}

	public Message update(String title, Message message)
	{
		
		var tempMessage = messageList.stream().filter(msg -> msg.getTitle().equals(title)).findFirst().get();
		messageList.remove(tempMessage);
		messageList.add(message);		
		return message;
	}
	
	public void delete(String title)
	{
		var tempMessage = messageList.stream().filter(msg -> msg.getTitle().equals(title)).findFirst().get();
		messageList.remove(tempMessage);
	}
}
