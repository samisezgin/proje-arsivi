package com.emlakcepte.model;

public class Message
{
	private String title;
	private String message;
	private User from;
	private User to;

	public Message(String title, String message, User from, User to)
	{
		super();
		this.title = title;
		this.message = message;
		this.from = from;
		this.to = to;
	}

	public User getFrom()
	{
		return from;
	}

	public void setFrom(User from)
	{
		this.from = from;
	}

	public String getTitle()
	{
		return title;
	}

	public void setTitle(String title)
	{
		this.title = title;
	}

	public String getMessage()
	{
		return message;
	}

	public void setMessage(String message)
	{
		this.message = message;
	}

	public User getTo()
	{
		return to;
	}

	public void setTo(User to)
	{
		this.to = to;
	}

}
