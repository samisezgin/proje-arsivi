package com.samisezgin.emlakburada.model;

import javax.persistence.*;

@Entity
@Table(name = "messages")
public class Message
{
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	@Column(name = "title")
	private String title;

	@Column(name = "content")
	private String content;

	@OneToOne
	@JoinColumn(name = "from_user_id")
	private User from;

	@OneToOne
	@JoinColumn(name = "to_user_id")
	private User to;

	public Message()
	{
		super();
	}

	public Message(String title, String content, User from, User to)
	{
		super();
		this.title = title;
		this.content = content;
		this.from = from;	
		this.to=to;
		
	}

	public String getTitle()
	{
		return title;
	}

	public void setTitle(String title)
	{
		this.title = title;
	}

	public String getContent()
	{
		return content;
	}

	public void setContent(String content)
	{
		this.content = content;
	}

	public User getFrom()
	{
		return from;
	}

	public void setFrom(User from)
	{
		this.from = from;
	}
	
	public Integer getId()
	{
		return id;
	}

	@Override
	public String toString()
	{
		return "Message [title=" + title + ", content=" + content + "]";
	}

}
