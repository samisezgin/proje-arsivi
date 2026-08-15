package com.clonemedium.controller;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.clonemedium.model.Tag;
import com.clonemedium.services.TagService;

@RestController
@RequestMapping("/tags")
public class TagController
{
	@Autowired
	private TagService tagService;
	
	@PostMapping
	public Tag create(Tag tag)
	{
		tagService.createTag(tag);
		return tag;
	}
	
	@DeleteMapping
	public void delete(Tag tag)
	{
		tagService.removeTag(tag);
	}
	
	@GetMapping
	public List<Tag> getAll()
	{
		return tagService.getAll();
	}
	
	
}
