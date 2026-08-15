package com.clonemedium.services;

import java.util.List;

import org.springframework.stereotype.Service;

import com.clonemedium.model.Blog;
import com.clonemedium.model.BlogStatus;
import com.clonemedium.model.Tag;
import com.clonemedium.repository.BlogRepository;

@Service
public class BlogService
{
	private BlogRepository blogDao = new BlogRepository();

	public Blog createBlog(Blog blog)
	{
		blogDao.createBlog(blog);
		return blog;
	}
	
	

	public boolean removeBlog(Blog blog)
	{
		return blogDao.removeBlog(blog);
	}

	public List<Blog> getAll()
	{
		return blogDao.getAll();
	}
	
	public void printAllBlogs()
	{
		blogDao.getAll().forEach(blog->System.out.println("Username: " + blog.getUser().getUserName() + "\tBlog Title: " + blog.getTitle()));
	}

	public void addBlogToTag(Blog blog, Tag tag)
	{
		blogDao.addBlogToTag(blog, tag);
	}

	public void removeBlogFromTag(Blog blog, Tag tag)
	{
		blogDao.removeBlogFromTag(blog, tag);
	}

	public void publishBlog(Blog blog)
	{
		blogDao.setBlogStatus(blog, BlogStatus.PUBLISHED);
	}

	public void deleteBlog(Blog blog)
	{
		blogDao.setBlogStatus(blog, BlogStatus.DELETED);
	}

	public void draftBlog(Blog blog)
	{
		blogDao.setBlogStatus(blog, BlogStatus.DRAFT);
	}

}
