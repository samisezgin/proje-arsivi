package com.clonemedium.services;

import java.util.List;

import org.springframework.stereotype.Service;

import com.clonemedium.model.Tag;
import com.clonemedium.repository.TagRepository;

@Service
public class TagService
{
	private TagRepository tagDao = new TagRepository();

	public Tag createTag(Tag tag)
	{		
		tagDao.createTag(tag);
		return tag;
	}

	public void removeTag(Tag tag)
	{
		tagDao.removeTag(tag);
	}

	public List<Tag> getAll()
	{
		return tagDao.getAll();
	}

	public void printAllTags()
	{
		getAll().forEach(tag->System.out.println(tag.getTagName()));
		
	}

	public void printBlogTitleByTag(Tag tag)
	{		
		getAll().forEach(tag1 -> tag1.getBlogs().stream().filter(blog->blog.getTag().getTagName().equals(tag.getTagName())).forEach(blog1->System.out.println(blog1.getTitle())));
	}
	
	

}
