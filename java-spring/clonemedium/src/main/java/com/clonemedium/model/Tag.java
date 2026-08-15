package com.clonemedium.model;

import java.util.List;

public class Tag
{
	private String tagName;
	private List<Blog> blogs;	
	

	public Tag()
	{
		super();
	}

	public Tag(String tagName, List<Blog> blogs)
	{
		super();
		this.tagName = tagName;
		this.blogs = blogs;
	}

	public List<Blog> getBlogs()
	{
		return blogs;
	}

	public void setBlogs(List<Blog> blogs)
	{
		this.blogs = blogs;
	}

	public String getTagName()
	{
		return tagName;
	}

	public void setTagName(String tagName)
	{
		this.tagName = tagName;
	}
}
