package com.clonemedium.model;

public class Blog
{
	private String title;
	private String content;
	private Tag tag;
	private User user;
	private BlogStatus blogStatus= BlogStatus.DRAFT;

	public Blog()
	{
		super();		
	}

	public Blog(String title, String content, User user)
	{
		this.title = title;
		this.content = content;
		this.tag = new Tag();
		this.user = user;		
	}

	public User getUser()
	{
		return user;
	}

	public void setUser(User user)
	{
		this.user = user;
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

	public Tag getTag()
	{
		return tag;
	}

	public void setTag(Tag tag)
	{
		this.tag = tag;
	}

	public BlogStatus getBlogStatus()
	{
		return blogStatus;
	}

	public void setBlogStatus(BlogStatus blogStatus)
	{
		this.blogStatus = blogStatus;
	}

}
