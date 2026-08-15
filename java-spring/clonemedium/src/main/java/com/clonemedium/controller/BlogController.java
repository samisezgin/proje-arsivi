package com.clonemedium.controller;

import java.util.List;
import java.util.Objects;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.clonemedium.model.Blog;
import com.clonemedium.model.BlogStatus;
import com.clonemedium.services.BlogService;

@RestController
@RequestMapping("/blogs")
public class BlogController
{
	@Autowired
	private BlogService blogService;
	
	@PostMapping
	public Blog create(Blog blog)
	{
		blogService.createBlog(blog);
		return blog;
	}
	
	@DeleteMapping
	public void delete(Blog blog)
	{
		blogService.deleteBlog(blog);
	}
	
	@GetMapping
	public List<Blog> getAll()
	{
		return blogService.getAll();
	}
	
	@PutMapping
	public Blog update(BlogStatus status, Blog blog)
	{
		Blog tempBlog = blogService.getAll().stream().filter(blg->blg.getTitle().equals(blog.getTitle())).findFirst().get();
		if(Objects.nonNull(tempBlog))
		{
			tempBlog.setBlogStatus(status);
		}
		return blog;
	}
	
	
	
	
}
